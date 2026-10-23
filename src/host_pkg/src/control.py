"""Result-driven process controller. No ROS or HTTP dependency; no timed success."""
from collections import deque
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import time
import uuid

DEVICES = ('M1', 'M2', 'arm1', 'arm2', 'arm3')
MANUAL_DESTINATIONS = {'GO_TO_MAT', 'GO_TO_ASM', 'GO_TO_REST', 'GO_TO_PARK'}
GROUPS = {'M1': ('M1',), 'M2': ('M2',), 'warehouse': ('arm1',), 'production': ('arm2', 'arm3')}


@dataclass(frozen=True)
class Step:
    device: str
    command: str
    product_no: int
    label: str


def make_plan(product, quantity, products=None):
    if product not in ('A', 'B') or type(quantity) is not int or quantity not in (1, 2):
        raise ValueError('A/B 제품과 수량 1/2만 지원합니다.')
    products = products if products is not None else [product] * quantity
    if not isinstance(products, list) or len(products) != quantity or any(p not in ('A', 'B') for p in products):
        raise ValueError('제품별 공정 목록 형식 오류')
    def step(device, command, number, label):
        if device.startswith('arm'):
            command = command.rsplit('_', 1)[0] + '_' + products[number - 1]
        return Step(device, command, number, label)
    plan = [step('M1', 'GO_TO_MAT', 1, 'M1 자재창고 도킹')]
    if quantity == 2:
        plan.append(step('M2', 'GO_TO_REST', 2, 'M2 대기장소 주차'))
    plan += [step('arm1', 'SELECT_' + product, 1, '1번 자재 적재'),
             step('M1', 'GO_TO_ASM', 1, 'M1 제작공정 도킹'),
             step('arm2', 'BUILD_' + product, 1, '1번 조립')]
    if quantity == 2:
        plan += [step('M2', 'GO_TO_MAT', 2, 'M2 자재창고 도킹'),
                 step('arm1', 'SELECT_' + product, 2, '2번 자재 적재')]
    plan.append(step('arm3', 'LOAD_' + product, 1, '1번 완제품 팔레트 적재'))
    if quantity == 2:
        plan += [step('M1', 'GO_TO_REST', 1, 'M1 대기장소 주차'),
                 step('M2', 'GO_TO_ASM', 2, 'M2 마지막 운송 도킹'),
                 step('M1', 'GO_TO_PARK', 1, 'M1 초기위치 복귀'),
                 step('arm2', 'BUILD_' + product, 2, '2번 조립'),
                 step('arm3', 'LOAD_' + product, 2, '2번 완제품 팔레트 적재'),
                 step('M2', 'GO_TO_PARK', 2, 'M2 초기위치 복귀')]
    else:
        plan.append(step('M1', 'GO_TO_PARK', 1, 'M1 초기위치 복귀'))
    return plan


class ProcessController:
    def __init__(self, transport, *, clock=time.monotonic, state_file=None,
                 goal_timeout=5.0, motion_timeout=300.0, arm_timeout=600.0, mode='hardware', manual_inspection=False):
        self.transport, self.clock = transport, clock
        self.state_file = Path(state_file) if state_file else None
        self.goal_timeout, self.motion_timeout, self.arm_timeout = goal_timeout, motion_timeout, arm_timeout
        self.mode = mode
        self.manual_inspection = manual_inspection
        self.order, self.active, self.plan = None, None, []
        self.ready = dict.fromkeys(DEVICES, False)
        self.link = False
        self.processed = deque(maxlen=256)
        self.rejected = deque(maxlen=256)
        self.log = deque(maxlen=50)
        self.device_logs = {device: deque(maxlen=25) for device in DEVICES}
        self.fault_device = None
        self.recovery_stop = None
        self.reset_stop_device = None
        self.stop_request = None
        self.reset_pending = False
        self.recovery_uncertain = False
        self.manual_revision = 0
        if self.state_file and self.state_file.exists():
            saved = json.loads(self.state_file.read_text())
            self.order = saved.get('order')
            self.manual_revision = saved.get('manual_revision', 0)
            self.processed.extend(saved.get('processed', []))
            self.rejected.extend(saved.get('rejected', []))
            self.log.extend(saved.get('log', []))
            if self.order:
                self.plan = ([Step(**step) for step in self.order['process_plan']]
                             if self.order.get('plan_mode') == 'continuous-v1' else
                             make_plan(self.order['product_type'], self.order['quantity'], self.order.get('products')))
                if self.order['status'] not in ('idle', 'done'):
                    self.order.update(status='failed', pause_requested=False,
                                      fault='이전 실행의 미완료 주문입니다. 장치 상태·초기 배치 복구가 필요합니다.')
                    self.recovery_stop = saved.get('active')
                    self.recovery_uncertain = bool(self.recovery_stop or saved.get('recovery_uncertain'))
                    self.reset_stop_device = saved.get('reset_stop_device') or (self.recovery_stop or {}).get('device')
                    if not self.recovery_stop and self.reset_stop_device:
                        self.recovery_stop = {'device': self.reset_stop_device}
                    self.note(self.order['fault'])
                    self.save()
            if (not self.order or self.order['status'] == 'done') and (
                    (saved.get('active') or {}).get('manual') or saved.get('recovery_uncertain')):
                self.recovery_stop = saved.get('active') or {'device': saved['reset_stop_device']}
                self.reset_stop_device = self.recovery_stop['device']
                self.recovery_uncertain = True
                self.note('이전 수동 이동 결과 미확인 · 정지 응답 확인 전 새 지시 보류')
                self.save()
            saved_task = saved.get('active') or {}
            if saved_task.get('preparation'):
                self.active = dict(saved_task, failed=True)
                self.recovery_stop = self.reset_stop_device = None
                self.recovery_uncertain = True
                self.note('이전 주차 준비 결과 미확인 · 원격 작업 종료 확인 필요, 자동 재실행 없음')
                self.save()

    def note(self, text, device=None):
        entry = f'{time.strftime("%H:%M:%S")} {text}'
        self.log.append(entry)
        if device:
            self.device_logs[device].append(entry)

    def save(self):
        if self.state_file:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.state_file.with_suffix('.tmp')
            with temporary.open('w') as stream:
                json.dump({'order': self.order, 'active': self.active or self.recovery_stop,
                           'manual_revision': self.manual_revision,
                           'reset_stop_device': self.reset_stop_device, 'recovery_uncertain': self.recovery_uncertain,
                           'processed': list(self.processed), 'rejected': list(self.rejected),
                           'log': list(self.log), **self.extra_state()}, stream, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.state_file)

    def extra_state(self):
        return {}

    def clear_extra_state(self):
        pass

    def command(self, command):
        command_id = command.get('id')
        if not isinstance(command_id, str) or not command_id:
            return
        if command_id in self.processed:
            return
        try:
            action = command.get('action')
            if self.manual_inspection and action in ('start','next','retry','resume'):
                raise ValueError('수동 점검 모드에서는 전체 공정을 실행하지 않습니다. 작업 종료 후 hostrun을 사용하세요.')
            if action == 'prepare_parked':
                if (not self.can_prepare_parked() or command.get('device') not in ('M1', 'M2')
                        or command.get('operator_confirmed') is not True
                        or command.get('order_id') != (self.order['id'] if self.order else None)
                        or type(command.get('recovery_revision')) is not int
                        or command['recovery_revision'] != self.manual_revision):
                    raise ValueError('실패 주문 초기화·작업 종료·지정 주차 위치와 방향 확인이 필요합니다.')
                self.manual_revision += 1
                self.active = dict(id=uuid.uuid4().hex, device=command['device'],
                                   command='PREPARE_PARKED', label=command['device']+' 주차 위치 초기화·준비',
                                   manual=True, preparation=True, standalone=True, accepted=True,
                                   submitted=self.clock(), accepted_at=self.clock(), last_seen=self.clock())
                self.save()
                self.note(self.active['label']+' 요청 · 이동 목표 없음', command['device'])
                try:
                    self.transport.prepare_parked(self.active.copy())
                except Exception as exc:
                    self.preparation_event('done', dict(success=False, uncertain=False, message=str(exc)))
            elif action == 'start':
                if not self.idle_available():
                    raise ValueError('수동 이동 또는 이전 지시의 종료·정지 확인이 필요합니다.')
                if self.order and self.order['status'] != 'done':
                    raise ValueError('진행 중이거나 복구가 필요한 주문이 있습니다.')
                plan = make_plan(command.get('product_type'), command.get('quantity'), command.get('products'))
                automatic = command.get('auto_advance', True)
                if type(automatic) is not bool:
                    raise ValueError('auto_advance는 boolean이어야 합니다.')
                if not self.link or not all(self.ready.values()):
                    raise ValueError('Host 연결과 다섯 장치의 Action 서버를 먼저 확인하세요.')
                self.plan = plan
                self.manual_revision += 1  # Invalidate a dialog opened before this order.
                self.fault_device = None
                self.order = {'id': uuid.uuid4().hex, 'product_type': command['product_type'],
                              'quantity': command['quantity'], 'status': 'running', 'stage': 0,
                              'stage_count': len(plan), 'completed': 0,
                              'product_remaining': command['quantity'], 'transport_remaining': command['quantity'],
                              'auto_advance': automatic, 'pause_requested': False, 'fault': ''}
                if 'products' in command:
                    self.order['products'] = list(command['products'])
                self.note(f"주문 {self.order['id']} · {command['product_type']} {command['quantity']}개")
            elif action == 'manual_move' and (not self.order or self.order['status'] == 'done'):
                expected_id = self.order['id'] if self.order else None
                expected_stage = self.order['stage'] if self.order else 0
                revision = self.order.get('recovery_revision', 0) if self.order else self.manual_revision
                if (not self.can_manual_move(command.get('device')) or command.get('operator_confirmed') is not True
                        or command.get('order_id') != expected_id
                        or type(command.get('stage')) is not int or command['stage'] != expected_stage
                        or type(command.get('recovery_revision')) is not int
                        or command['recovery_revision'] != revision):
                    raise ValueError('주문 대기·작업 종료·현장 상태를 다시 확인하세요.')
                self.validate_manual(command)
                if self.order:
                    self.order['recovery_revision'] = revision + 1
                else:
                    self.manual_revision += 1
                self.send_manual(command, standalone=True)
            else:
                if not self.order or command.get('order_id') != self.order['id']:
                    raise ValueError('현재 주문 ID와 일치하지 않습니다.')
                status = self.order['status']
                if action in ('retry', 'manual_move'):
                    if (not (self.can_manual_move(command.get('device')) if action == 'manual_move' else self.can_recover()) or command.get('operator_confirmed') is not True
                            or type(command.get('stage')) is not int or command['stage'] != self.order['stage']
                            or type(command.get('recovery_revision')) is not int
                            or command['recovery_revision'] != self.order.get('recovery_revision', 0)):
                        raise ValueError('실패 단계·작업 종료·현장 상태를 다시 확인하세요.')
                    if action == 'manual_move' and (command.get('device') not in ('M1', 'M2')
                            or command.get('destination') not in MANUAL_DESTINATIONS):
                        raise ValueError('M1/M2와 지정된 네 목적지만 지원합니다.')
                    self.order['recovery_revision'] = self.order.get('recovery_revision', 0) + 1
                    # A terminal Result plus explicit physical confirmation permits recovery.
                    # Never release a robot stop lock or reset its pose automatically.
                    self.reset_stop_device = None
                    if action == 'retry':
                        self.order.update(status='running', fault='', pause_requested=False)
                        self.fault_device = None
                        self.note('현장 확인 후 실패 단계 재시도 · ' + ('성공 후 자동 진행' if self.order['auto_advance'] else '성공 후 다음 단계 대기'))
                    else:
                        self.send_manual(command)
                elif action == 'reset':
                    if command.get('operator_confirmed') is not True:
                        raise ValueError('로봇 정지·작업 종료·초기 배치를 현장에서 확인하세요.')
                    if not self.can_reset():
                        raise ValueError('실패 주문·장치 연결·이전 지시 응답을 확인한 뒤 초기화하세요.')
                    device = self.reset_stop_device or (self.active or {}).get('device')
                    if device:
                        self.reset_pending = True
                        self.note('초기화 대기 · 실패 장치의 정지 응답 확인 중')
                        self.request_stop(device)
                    else:
                        self.finish_reset()
                elif action == 'next':
                    if status != 'waiting' or command.get('stage') != self.order['stage'] or not self.can_advance():
                        raise ValueError('다음 단계 조건 또는 단계 번호 불일치')
                    self.order['status'] = 'running'
                elif action == 'pause':
                    if status not in ('running', 'waiting'):
                        raise ValueError('현재 상태에서는 일시정지할 수 없습니다.')
                    self.order['pause_requested'] = True
                    if not self.active:
                        self.order['status'] = 'paused'
                    self.note('현재 동작 완료 후 다음 단계 진입 보류')
                elif action == 'resume':
                    if status != 'paused' or not self.link or not all(self.ready.values()):
                        raise ValueError('연결·장치 준비·일시정지 상태를 확인하세요.')
                    self.order['pause_requested'] = False
                    self.order['status'] = 'running' if self.order['auto_advance'] else 'waiting'
                    self.note('사용자 재개 요청')
                else:
                    raise ValueError('지원하지 않는 명령')
        except (ValueError, TypeError, OSError) as exc:
            self.rejected.append(command_id)
            self.note(f'지시 거절 {command_id}: {exc}')
        self.processed.append(command_id)
        self.save()

    def can_advance(self):
        return bool(self.order and self.order['status'] == 'waiting' and not self.active
                    and self.link and all(self.ready.values()))

    def idle_available(self):
        return bool(self.link and all(self.ready.values()) and not self.active
                    and not self.recovery_stop and not self.recovery_uncertain
                    and not self.stop_request and not self.reset_pending)

    def can_manual_move(self, device=None):
        if device is None:
            return any(self.can_manual_move(robot) for robot in ('M1', 'M2'))
        if device not in ('M1', 'M2'): return False
        if not self.manual_inspection:
            if self.order and self.order['status'] != 'done': return self.can_recover()
            return self.idle_available() and bool(self.ready.get(device))
        if self.order and self.order['status'] not in ('done','failed'): return False
        # Standalone inspection requires the selected AMR, not unrelated cells.
        # Outstanding operations still reserve the whole host.
        return bool(self.link and self.ready.get(device) and not self.active
                    and not self.recovery_stop and not self.recovery_uncertain
                    and not self.stop_request and not self.reset_pending
                    and not getattr(self, 'parallel_blocked', lambda: False)()
                    and not getattr(self, 'reset_busy', lambda: False)())

    def can_prepare_parked(self):
        # Robot Action discovery may be absent just after power-on. The SSH
        # readiness workflow checks actual motion, sensors and torque itself.
        return bool(self.mode == 'hardware' and self.link
                    and (not self.order or self.order['status'] == 'done')
                    and not self.active and not self.recovery_stop and not self.recovery_uncertain
                    and not self.stop_request and not self.reset_pending
                    and not getattr(self, 'parallel_blocked', lambda: False)())

    def preparation_event(self, kind, data):
        if kind != 'done':
            return
        task = self.active
        success = data.get('success') is True and not data.get('uncertain')
        self.note(task['label'] + (' 완료 · 이동 목표 없음' if success else
                  ' 실패 · '+str(data.get('message', '결과 확인 필요'))), task['device'])
        if data.get('uncertain'):
            # SSH loss/timeout is not evidence the remote preparation ended.
            # Keep the reservation; never retry or unlock on a local timer.
            task['failed'] = True
            self.recovery_uncertain = True
        else:
            self.active = None
        self.save()

    @staticmethod
    def validate_manual(command):
        if command.get('device') not in ('M1', 'M2') or command.get('destination') not in MANUAL_DESTINATIONS:
            raise ValueError('M1/M2와 지정된 네 목적지만 지원합니다.')

    def send_manual(self, command, standalone=False):
        device, destination = command['device'], command['destination']
        self.active = dict(id=uuid.uuid4().hex, device=device, command=destination,
                           label=f'{device} 수동 이동 {destination}', manual=True, standalone=standalone,
                           accepted=False, submitted=self.clock(), last_seen=self.clock())
        self.save()  # Record before sending, including when there is no order.
        self.note(self.active['label'] + (' 요청 · 개별 동작' if standalone else ' 요청 · 주문 단계 유지'), device)
        try:
            self.transport.send(self.active.copy())
        except Exception as exc:
            self.fail_manual(f'수동 이동 전송 오류: {exc}')

    def can_recover(self):
        return bool(self.order and self.order['status'] == 'failed'
                    and 0 <= self.order['stage'] < len(self.plan)
                    and self.link and all(self.ready.values()) and not self.active
                    and not self.recovery_stop and not self.recovery_uncertain and not self.stop_request and not self.reset_pending)

    def fail_manual(self, reason):
        if not self.active or self.active.get('failed'):
            return
        self.active['failed'] = True
        if self.active.get('standalone'):
            self.recovery_uncertain = True
        self.note(reason + (' · 개별 동작 중단' if self.active.get('standalone') else ' · 주문은 실패 상태 유지'), self.active['device'])
        self.request_stop(self.active['device'])

    def manual_event(self, request_id, kind, data):
        task = self.active
        if kind == 'accepted':
            if task.get('failed'):
                self.request_stop(task['device'])
            elif not task['accepted']:
                task.update(accepted=True, accepted_at=self.clock())
                self.note('수동 이동 접수 · ' + task['command'], task['device'])
        elif kind == 'feedback':
            if data.get('message') in ('ERROR', 'PAUSED'):
                self.fail_manual('수동 이동 오류 · ' + data['message'])
        elif kind == 'done':
            success = (task['accepted'] and not task.get('failed') and data.get('status') == 4
                       and data.get('success') is True and data.get('message') == 'IDLE')
            self.note('수동 이동 ' + ('완료' if success else '실패') + ' · ' + task['command']
                      + ' · ' + str(data.get('message', '')), task['device'])
            if data.get('uncertain'):
                self.fail_manual('수동 이동 결과 미확인')
            else:
                if task.get('standalone'):
                    self.recovery_uncertain = False  # A definitive terminal result, never a timer.
                self.active = None
        self.save()

    def can_reset(self):
        return bool(self.order and self.order['status'] == 'failed'
                    and self.link and all(self.ready.values()) and not self.reset_pending
                    and not self.stop_request and not (self.active or {}).get('manual')
                    and (not self.active or self.active['accepted']))

    def finish_reset(self):
        # Preserve the failed order before releasing the interlock. No movement,
        # torque enable, stop unlock, or pose reset is issued here.
        identity = self.order['id']
        if self.state_file:
            archive = self.state_file.parent / 'order-history'
            archive.mkdir(parents=True, exist_ok=True)
            target = archive / (time.strftime('%Y%m%d-%H%M%S-') + uuid.uuid4().hex + '.json')
            with target.open('x') as stream:
                json.dump({'order': self.order, 'active': self.active,
                           'log': list(self.log), 'operator_confirmed': True,
                           **self.extra_state()}, stream, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
        self.clear_extra_state()
        self.order, self.active, self.plan = None, None, []
        self.manual_revision += 1
        self.fault_device = self.recovery_stop = self.reset_stop_device = None
        self.reset_pending = False
        self.recovery_uncertain = False
        self.note(f'실패 주문 초기화 · {identity} · 현장 확인 완료, 새 이동 전송 없음')
        self.save()

    def fail(self, reason, uncertain=False):
        if not self.order or self.order['status'] in ('done', 'failed'):
            return
        self.order.update(status='failed', pause_requested=False, fault=reason)
        self.fault_device = self.active['device'] if self.active else None
        self.note('공정 실패 · ' + reason, self.fault_device)
        self.save()
        if uncertain and self.active:
            self.request_stop(self.active['device'])

    def request_stop(self, device):
        self.reset_stop_device = device
        self.save()
        self.note('EMER_STOP 요청 · 확인 전까지 정지 여부 미확인 (리니어 제외)', device)
        self.stop_request = (self.transport.stop(device), device, self.clock())

    def event(self, request_id, kind, data):
        if kind == 'stop':
            confirmed = data.get('success') is True and data.get('status') == 4 and data.get('message') == 'IDLE'
            self.note('정지 응답 확인 (리니어 제외)' if confirmed else '정지 여부 미확인: ' + str(data.get('message')), data['device'])
            expected = self.stop_request
            if expected and expected[1] == data['device'] and (expected[0] is None or expected[0] == request_id):
                self.stop_request = None
                if confirmed:
                    self.recovery_uncertain = False
                    self.reset_stop_device = None
                if self.reset_pending:
                    self.reset_pending = False
                    if confirmed:
                        try:
                            self.finish_reset()
                        except OSError as exc:
                            self.note(f'초기화 보류 · 기록 보관 실패: {exc}')
                    else:
                        self.note('초기화 보류 · 정지 응답 미확인, 연결과 현장 상태를 확인하세요.')
            self.save()
            return
        if not self.active or request_id != self.active['id']:
            return  # delayed or duplicate results cannot complete another step/order
        device = self.active['device']
        if self.active.get('preparation'):
            self.preparation_event(kind, data)
            return
        if self.active.get('manual'):
            self.manual_event(request_id, kind, data)
            return
        if self.order['status'] == 'failed':
            if kind == 'accepted':
                self.request_stop(device)  # late acceptance after a timeout must not escape the stop
            if kind == 'done':
                self.active = None
                self.save()
            return
        if kind == 'accepted':
            if not self.active['accepted']:
                self.active['accepted'] = True
                self.active['accepted_at'] = self.clock()
                if self.active['command'] == 'GO_TO_ASM':
                    # Re-acceptance of the same failed stage must not count twice.
                    accepted_transports = sum(step.command == 'GO_TO_ASM'
                                              for step in self.plan[:self.order['stage'] + 1])
                    self.order['transport_remaining'] = self.order['quantity'] - accepted_transports
                self.note(f"접수 {self.active['command']} · 작업 {request_id}", device)
                self.save()
        elif kind == 'feedback':
            message = data.get('message', '')
            if message != self.active.get('feedback'):
                self.active['feedback'] = message
                self.note('Feedback ' + message, device)
                if message in ('PAUSED', 'ERROR'):
                    self.fail('장치가 작업 보류 또는 오류를 보고했습니다. 현장 상태를 확인하세요.', uncertain=True)
        elif kind == 'done':
            success = (self.active['accepted'] and data.get('status') == 4
                       and data.get('success') is True and data.get('message') == 'IDLE')
            if not success:
                self.fail(f"{device} {self.active['command']}: {data.get('message', '결과 오류')}",
                          uncertain=bool(data.get('uncertain')))
                if not data.get('uncertain'):
                    self.active = None
                    self.save()
                return
            if self.active['command'] in ('LOAD_A', 'LOAD_B'):
                self.order['completed'] += 1
                self.order['product_remaining'] -= 1
            self.note(f"완료 {self.active['label']} · 작업 {request_id}", device)
            self.order['stage'] += 1
            self.active = None
            if self.order['stage'] == len(self.plan):
                self.order.update(status='done', pause_requested=False)
                self.note('주문 완료 · 모든 적재 및 운송 로봇 복귀 Result 확인')
            elif self.order['pause_requested']:
                self.order['status'] = 'paused'
            elif not self.order['auto_advance']:
                self.order['status'] = 'waiting'
            self.save()

    def tick(self, link):
        self.link = link
        self.ready = self.transport.ready()
        if self.active and self.active.get('preparation'):
            # Preparation owns service setup and can temporarily lose DDS.
            # Its correlated subprocess result, not Action discovery, ends it.
            return
        if self.stop_request and self.clock() - self.stop_request[2] > 15:
            self.stop_request = None
            self.reset_pending = False
            self.note('정지 응답 시간 초과 · 초기화 보류')
            self.save()
        if self.recovery_stop and self.ready.get(self.recovery_stop['device']):
            device = self.recovery_stop['device']
            self.recovery_stop = None
            self.request_stop(device)
        if self.active and self.active.get('manual'):
            task = self.active
            if not task.get('failed'):
                if self.ready[task['device']]:
                    task['last_seen'] = self.clock()
                if not link or self.clock() - task['last_seen'] > self.goal_timeout:
                    self.fail_manual('수동 이동 중 연결 끊김')
                elif not task['accepted'] and self.clock() - task['submitted'] > self.goal_timeout:
                    self.fail_manual('수동 이동 접수 시간 초과')
                elif task['accepted'] and self.clock() - task['accepted_at'] > self.motion_timeout:
                    self.fail_manual('수동 이동 결과 시간 초과')
            return
        if not self.order or self.order['status'] in ('done', 'failed'):
            return
        if not link and self.order['status'] in ('running', 'waiting'):
            if not self.order['pause_requested']:
                self.note('웹 API 연결 끊김 · 현재 동작 완료 후 보류, 자동 재개 안 함')
                self.order['pause_requested'] = True
                if not self.active:
                    self.order['status'] = 'paused'
                self.save()
        if self.active:
            if self.ready[self.active['device']]:
                self.active['last_seen'] = self.clock()
            if self.clock() - self.active['last_seen'] > self.goal_timeout:
                self.fail('실행 장치 Action 서버 연결 끊김', uncertain=True)
            elif not self.active['accepted'] and self.clock() - self.active['submitted'] > self.goal_timeout:
                self.fail('Action 접수 응답 시간 초과', uncertain=True)
            elif self.active['accepted']:
                limit = self.motion_timeout if self.active['device'] in ('M1', 'M2') else self.arm_timeout
                if self.clock() - self.active['accepted_at'] > limit:
                    self.fail('Action 최종 결과 시간 초과', uncertain=True)
            return
        if self.order['status'] != 'running' or not link or self.order['pause_requested']:
            return
        if not all(self.ready.values()):
            self.order.update(status='paused', pause_requested=True)
            self.note('장치 서버 미연결 · 다음 동작 보류')
            self.save()
            return
        step = self.plan[self.order['stage']]
        self.active = dict(asdict(step), id=uuid.uuid4().hex, accepted=False,
                           submitted=self.clock(), last_seen=self.clock())
        self.save()  # journal before side effect; never auto-replay after a restart
        self.note(f'요청 {step.device} {step.command}', step.device)
        try:
            self.transport.send(self.active.copy())
        except Exception as exc:
            self.fail(f'Action 전송 오류: {exc}', uncertain=True)

    def snapshot(self):
        devices = {}
        for group, members in GROUPS.items():
            state, detail = 'idle', 'Action 서버 연결 · 명령 대기'
            if not all(self.ready[member] for member in members):
                state, detail = 'offline', 'Action 서버 연결 대기'
            if self.active and self.active['device'] in members:
                state, detail = 'running', self.active['label']
            if self.fault_device in members and not (self.active or {}).get('manual'):
                state, detail = 'failed', self.order['fault']
            devices[group] = {'state': state, 'detail': detail,
                              'log': [line for member in members for line in self.device_logs[member]][-50:]}
        order = dict(self.order) if self.order else None
        if order:
            order['stage_label'] = (self.active['label'] if self.active else
                                    self.plan[order['stage']].label if order['stage'] < len(self.plan) else '전체 완료')
        conditions = [{'label': '다섯 장치 Action 서버 연결', 'done': all(self.ready.values())}]
        if self.manual_inspection:
            conditions = [{'label': robot+' 개별 수동 이동 가능', 'done': self.can_manual_move(robot)} for robot in ('M1','M2')]
        if order:
            conditions.append({'label': '현재 작업의 최종 성공 Result 확인', 'done': not self.active and order['status'] in ('waiting', 'paused', 'done')})
        return {'devices': devices, 'order': order, 'conditions': conditions,
                'can_advance': not self.manual_inspection and self.can_advance(), 'can_start': bool(not self.manual_inspection and self.idle_available() and (not order or order['status'] == 'done')),
                'can_reset': self.can_reset(), 'reset_pending': self.reset_pending,
                'can_retry': not self.manual_inspection and self.can_recover(), 'can_manual_move': self.can_manual_move(),
                'manual_move_available': {robot: self.can_manual_move(robot) for robot in ('M1','M2')},
                'can_prepare_parked': self.can_prepare_parked(),
                'manual_revision': self.manual_revision,
                'manual_move': ({key: self.active.get(key) for key in ('id', 'device', 'command', 'label', 'failed')}
                                if self.active and self.active.get('manual') else None),
                'accepted_command_ids': list(self.processed),
                'rejected_command_ids': [identity for identity in self.rejected if identity in self.processed],
                'log': list(self.log), 'runtime_mode': self.mode, 'manual_inspection': self.manual_inspection}
