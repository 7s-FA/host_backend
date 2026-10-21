"""Dependency-gated production scheduling; older orders retain the serial engine.

One AMR owns the shared aisle. Arm2/arm3 share the assembly cell. Departure
may overlap arm3 loading: the operator confirmed these physical envelopes are
separate on 2026-10-20. This is a fixed layout contract, not collision detection.
"""
from dataclasses import asdict, replace
import json
from pathlib import Path
import uuid

from control import ProcessController, Step, make_plan

PLAN_MODE = 'parallel-v1'


def make_parallel_plan(product, quantity):
    return [replace(step, command='BUILD_LOAD_' + product,
                    label=f'{step.product_no}번 조립·적재 연속') if step.device == 'arm2' else step
            for step in make_plan(product, quantity)] + [Step('arm2', 'BUILD_SLIDE', 0, '리니어 조립 위치 사전 준비')]


def load_index(quantity, build_index):
    return {3: 4}[build_index] if quantity == 1 else {4: 7, 11: 12}[build_index]


def dependencies(quantity):
    if quantity == 1:
        # dock material -> load -> dock assembly -> build -> [pallet load, park]
        return (set(), {0}, {1}, {2, 6}, {3}, {3}, set())
    return (set(), {0}, {0}, {1, 2}, {3, 14}, {3}, {5}, {4},
            {4, 5}, {6, 7, 8}, {9}, {9}, {11}, {10, 11}, set())


def resources(step):
    if step.device in ('M1', 'M2'):
        return {step.device, 'shared_aisle'}
    if step.device in ('arm2', 'arm3'):
        return {step.device, 'assembly_cell'}
    return {step.device, 'warehouse_cell'}


class ParallelProcessController(ProcessController):
    def __init__(self, *args, **kwargs):
        self.inflight = {}
        self.finished = set()
        self.accepted_transports = set()
        self.failed_steps = set()
        self.parallel_stops = {}
        self.pending_stops = set()
        self.unconfirmed = set()
        self.stopped = set()
        self.orphans = {}
        path = kwargs.get('state_file')
        saved = json.loads(Path(path).read_text()) if path and Path(path).exists() else {}
        self.restoring = True
        super().__init__(*args, **kwargs)
        self.restoring = False
        if self.parallel_order():
            self.plan = make_parallel_plan(self.order['product_type'], self.order['quantity'])
            state = saved.get('parallel_state', {})
            self.finished = set(state.get('finished', []))
            self.accepted_transports = set(state.get('accepted_transports', []))
            self.failed_steps = set(state.get('failed_steps', []))
            self.orphans = dict(state.get('orphans', {}))
            self.orphans.update(state.get('inflight', {}))
            self.unconfirmed = set(state.get('unconfirmed', []))
            self.unconfirmed.update(state.get('pending_stops', []))
            self.unconfirmed.update(state.get('parallel_stops', {}))
            self.unconfirmed.update(task['device'] for task in self.orphans.values())
            self.pending_stops = self.unconfirmed.copy()
            # Legacy restart handling knows only one task; this engine tracks all.
            # Keep it for an independent manual move made after a failed/done order.
            if not (saved.get('active') or {}).get('manual'):
                self.active = self.recovery_stop = self.reset_stop_device = None
                self.recovery_uncertain = bool(self.unconfirmed)
            self.save()

    def parallel_order(self):
        return bool(self.order and self.order.get('plan_mode') == PLAN_MODE)

    def extra_state(self):
        return {'parallel_state': {
            'inflight': self.inflight, 'finished': sorted(self.finished),
            'accepted_transports': sorted(self.accepted_transports),
            'failed_steps': sorted(self.failed_steps), 'orphans': self.orphans,
            'parallel_stops': self.parallel_stops,
            'pending_stops': sorted(self.pending_stops), 'unconfirmed': sorted(self.unconfirmed)}}

    def save(self):
        if not self.restoring:
            super().save()

    def sync_active(self):
        self.active = next(iter(self.inflight.values()), None)
        # A manual move uses the serial stop journal even on a parallel order.
        # Never erase its unresolved restart/stop state while synchronizing tasks.
        self.recovery_uncertain = bool(self.unconfirmed or self.orphans or
                                       (self.reset_stop_device and self.recovery_uncertain))

    def parallel_blocked(self):
        return bool(self.inflight or self.orphans or self.parallel_stops or
                    self.pending_stops or self.unconfirmed)

    def idle_available(self):
        return super().idle_available() and not self.parallel_blocked()

    def can_recover(self):
        return super().can_recover() and not self.parallel_blocked()

    def can_reset(self):
        if not self.parallel_order():
            return super().can_reset()
        return bool(self.order['status'] == 'failed' and self.link and all(self.ready.values())
                    and not self.reset_pending and not self.parallel_stops and not self.pending_stops
                    and not self.stop_request and not self.recovery_stop
                    and not (self.active or {}).get('manual')
                    and all(t['accepted'] for t in self.inflight.values()))

    def command(self, command):
        action = command.get('action')
        identity = command.get('id')
        if not isinstance(identity, str) or not identity or identity in self.processed:
            return
        if action == 'reset' and self.parallel_order() and self.reset_stop_device:
            # An interrupted independent manual move retains the legacy stop
            # handshake; reset cannot clear it without that device's response.
            return super().command(command)
        if action == 'reset' and self.parallel_order():
            if (command.get('order_id') == self.order['id'] and command.get('operator_confirmed') is True
                    and self.can_reset()):
                devices = self.unconfirmed | {t['device'] for t in self.inflight.values()} | {t['device'] for t in self.orphans.values()}
                if devices:
                    self.reset_pending = True
                    for device in sorted(devices):
                        self.request_parallel_stop(device)
                else:
                    self.finish_reset()
            else:
                self.rejected.append(identity)
                self.note('초기화 거절 · 병렬 작업 전체의 종료·정지 응답과 현장 확인 필요')
            self.processed.append(identity)
            self.save()
            return
        super().command(command)
        if identity in self.rejected:
            return
        if action == 'start':
            self.finished.clear()
            self.accepted_transports.clear()
            self.failed_steps.clear()
            self.stopped.clear()
            self.order['plan_mode'] = PLAN_MODE
            self.plan = make_parallel_plan(self.order['product_type'], self.order['quantity'])
            self.order['stage_count'] = len(self.plan)
            self.note('병렬 공정 · 선행 Result 확인 · 공용 통로는 이동로봇 한 대만 사용')
            self.save()
        elif action == 'retry' and self.parallel_order():
            self.failed_steps.clear()
            self.save()

    def clear_extra_state(self):
        # Base archives the complete journal before invoking this atomic reset hook.
        self.inflight.clear()
        self.finished.clear()
        self.accepted_transports.clear()
        self.failed_steps.clear()
        self.parallel_stops.clear()
        self.pending_stops.clear()
        self.unconfirmed.clear()
        self.stopped.clear()
        self.orphans.clear()

    def request_parallel_stop(self, device, force=False):
        if device in self.parallel_stops and not force:
            return
        self.stopped.discard(device)
        self.unconfirmed.add(device)
        self.pending_stops.add(device)
        self.save()  # A restart must retain every possibly moving device.
        if not self.ready.get(device):
            return
        try:
            request = self.transport.stop(device)
        except Exception as exc:
            self.note(f'{device} 정지 전송 오류 · {exc}', device)
            return
        self.parallel_stops[device] = (request, self.clock())
        self.pending_stops.discard(device)
        self.note('병렬 작업 EMER_STOP 요청 · 최종 응답 확인 필요 (리니어 제외)', device)
        self.save()

    def fail(self, reason, uncertain=False, device=None):
        if not self.parallel_order() or (self.active or {}).get('manual'):
            return super().fail(reason, uncertain=uncertain)
        if self.order['status'] in ('done', 'failed'):
            return
        self.order.update(status='failed', pause_requested=False, fault=reason)
        self.fault_device = device or (self.active or {}).get('device')
        self.note('병렬 공정 실패 · ' + reason, self.fault_device)
        self.save()
        # No new dependencies launch after failure; stop every outstanding actor.
        for task in list(self.inflight.values()):
            self.request_parallel_stop(task['device'])
        self.sync_active()
        self.save()

    def event(self, request_id, kind, data):
        if (not self.parallel_order() or (self.active or {}).get('manual')
                or (kind == 'stop' and self.stop_request)):
            return super().event(request_id, kind, data)
        if kind == 'stop':
            device = data.get('device')
            expected = self.parallel_stops.get(device)
            if not expected or (expected[0] is not None and expected[0] != request_id):
                return
            del self.parallel_stops[device]
            confirmed = data.get('status') == 4 and data.get('success') is True and data.get('message') == 'IDLE'
            if confirmed:
                self.unconfirmed.discard(device)
                self.stopped.add(device)
                self.orphans = {key: task for key, task in self.orphans.items() if task['device'] != device}
            elif self.reset_pending:
                self.reset_pending = False
            self.note('병렬 작업 정지 응답 확인 (리니어 제외)' if confirmed else '병렬 작업 정지 미확인', device)
            self.sync_active()
            if self.reset_pending and not (self.parallel_stops or self.pending_stops or self.unconfirmed or self.orphans):
                try:
                    self.finish_reset()
                except OSError as exc:
                    self.reset_pending = False
                    self.note(f'초기화 보류 · 기록 보관 실패: {exc}')
            self.save()
            return
        task = self.inflight.get(request_id)
        if not task:
            return  # Old attempts and duplicated results never complete a new task.
        index, device = task['index'], task['device']
        if kind == 'accepted':
            if not task['accepted']:
                task.update(accepted=True, accepted_at=self.clock())
                if task['command'] == 'GO_TO_ASM':
                    self.accepted_transports.add(index)
                    self.order['transport_remaining'] = self.order['quantity'] - len(self.accepted_transports)
                self.note(f"접수 {task['command']} · 작업 {request_id}", device)
            if self.order['status'] == 'failed':
                self.request_parallel_stop(device, force=True)
        elif kind == 'feedback':
            message = data.get('message', '')
            if message != task.get('feedback'):
                task['feedback'] = message
                self.note('Feedback ' + message, device)
            if (message == 'BUILD_DONE' and task['command'].startswith('BUILD_LOAD_')
                    and task['accepted'] and not task.get('invalid')):
                # Goal-correlated phase evidence permits departure, not product
                # completion. Keep the cell reserved until the chain Result.
                self.finished.add(index)
                task['build_done'] = True
                task['label'] = f"{task['product_no']}번 완제품 적재 · 연속 작업"
                self.order['stage'] = len(self.finished)
            if message in ('ERROR', 'PAUSED'):
                task['invalid'] = True
                self.failed_steps.add(load_index(self.order['quantity'], index) if task.get('build_done') else index)
                self.fail(f'{device} {message} · 현장 확인 필요', uncertain=True, device=device)
        elif kind == 'done':
            success = (task['accepted'] and not task.get('invalid') and not data.get('uncertain')
                       and data.get('status') == 4 and data.get('success') is True and data.get('message') == 'IDLE')
            if data.get('uncertain'):
                task['invalid'] = True
                self.failed_steps.add(load_index(self.order['quantity'], index) if task.get('build_done') else index)
                self.fail(f'{device} 결과 미확인', uncertain=True, device=device)
            else:
                del self.inflight[request_id]
                self.unconfirmed.discard(device)  # Definitive terminal result, never elapsed time.
                if success:
                    self.finished.add(index)
                    self.failed_steps.discard(index)
                    if task['command'].startswith('BUILD_LOAD_'):
                        loading = load_index(self.order['quantity'], index)
                        self.finished.add(loading)
                        self.failed_steps.discard(loading)
                    if task['command'].startswith(('LOAD_', 'BUILD_LOAD_')):
                        self.order['completed'] += 1
                        self.order['product_remaining'] -= 1
                    self.note(f"완료 {task['label']} · 작업 {request_id}", device)
                else:
                    self.failed_steps.add(load_index(self.order['quantity'], index) if task.get('build_done') else index)
                    self.fail(f"{device} {task['command']}: {data.get('message', '결과 오류')}", device=device)
                self.order['stage'] = len(self.finished)
                self.sync_active()
                if self.order['status'] != 'failed':
                    if len(self.finished) == len(self.plan):
                        self.order.update(status='done', pause_requested=False)
                        self.note('주문 완료 · 모든 병렬 작업·적재·복귀 Result 확인')
                    elif not self.inflight:
                        if self.order['pause_requested']:
                            self.order['status'] = 'paused'
                        elif not self.order['auto_advance']:
                            self.order['status'] = 'waiting'
        self.sync_active()
        self.save()

    def tick(self, link):
        if (not self.parallel_order() or (self.active or {}).get('manual') or self.recovery_stop
                or self.stop_request or (self.reset_stop_device and self.recovery_uncertain)):
            return super().tick(link)
        self.link, self.ready = link, self.transport.ready()
        for device, (_, submitted) in list(self.parallel_stops.items()):
            if self.clock() - submitted > 15:
                del self.parallel_stops[device]
                self.reset_pending = False
                self.note('병렬 작업 정지 응답 시간 초과 · 자동 진행 금지', device)
                self.save()
        for device in list(self.pending_stops):
            self.request_parallel_stop(device)
        if self.order['status'] in ('done', 'failed'):
            self.sync_active()
            return
        if not link and self.order['status'] in ('running', 'waiting') and not self.order['pause_requested']:
            self.order['pause_requested'] = True
            self.note('웹 연결 끊김 · 실행 중 병렬 작업 완료 후 보류, 자동 재개 안 함')
            self.save()
        for task in list(self.inflight.values()):
            if self.ready[task['device']]:
                task['last_seen'] = self.clock()
            reason = None
            if self.clock() - task['last_seen'] > self.goal_timeout:
                reason = 'Action 서버 연결 끊김'
            elif not task['accepted'] and self.clock() - task['submitted'] > self.goal_timeout:
                reason = 'Action 접수 시간 초과'
            elif task['accepted']:
                limit = self.motion_timeout if task['device'] in ('M1', 'M2') else self.arm_timeout
                if self.clock() - task['accepted_at'] > limit:
                    reason = 'Action 최종 결과 시간 초과'
            if reason:
                task['invalid'] = True
                self.failed_steps.add(load_index(self.order['quantity'], task['index'])
                                      if task.get('build_done') else task['index'])
                self.fail(f"{task['device']} {reason}", uncertain=True, device=task['device'])
                return
        if self.order['pause_requested']:
            if not self.inflight and self.order['status'] != 'paused':
                self.order['status'] = 'paused'
                self.save()
            return
        if self.order['status'] != 'running' or not link:
            return
        if not all(self.ready.values()):
            self.order['pause_requested'] = True
            if not self.inflight:
                self.order['status'] = 'paused'
            self.note('장치 미연결 · 새 병렬 작업 보류')
            self.save()
            return
        if self.inflight and not self.order['auto_advance']:
            return  # Manual next launches one eligible wave, then waits for every Result.
        occupied = set().union(*(resources(self.plan[t['index']]) for t in self.inflight.values()))
        active_indices = {t['index'] for t in self.inflight.values()}
        for index, prerequisites in enumerate(dependencies(self.order['quantity'])):
            if index in self.finished or index in active_indices or not prerequisites <= self.finished:
                continue
            step = self.plan[index]
            claims = resources(step)
            if claims & occupied:
                continue
            task = dict(asdict(step), index=index, id=uuid.uuid4().hex, accepted=False,
                        submitted=self.clock(), last_seen=self.clock())
            self.inflight[task['id']] = task
            self.stopped.discard(step.device)
            self.sync_active()
            self.save()  # Persist each member before its own side effect.
            self.note(f'요청 {step.device} {step.command} · 선행 조건 완료', step.device)
            try:
                self.transport.send(task.copy())
            except Exception as exc:
                task['invalid'] = True
                self.failed_steps.add(index)
                self.fail(f'Action 전송 오류: {exc}', uncertain=True, device=step.device)
                return
            occupied.update(claims)

    def snapshot(self):
        report = super().snapshot()
        if not self.parallel_order():
            return report
        if not (self.active or {}).get('manual'):
            order = report['order']
            labels = [task['label'] for task in self.inflight.values()]
            if labels:
                order['stage_label'] = ('동시 작업 · ' if len(labels) > 1 else '') + ' + '.join(labels)
            elif order['status'] == 'failed':
                indices = sorted(self.failed_steps) or [i for i in range(len(self.plan)) if i not in self.finished]
                order['stage_label'] = ' / '.join(self.plan[i].label for i in indices)[:200]
            elif order['status'] != 'done':
                order['stage_label'] = ' + '.join(self.plan[i].label for i, deps in enumerate(dependencies(order['quantity']))
                                                 if i not in self.finished and deps <= self.finished)
            from control import GROUPS
            for group, members in GROUPS.items():
                active = [t['label'] for t in self.inflight.values() if t['device'] in members]
                if active and self.fault_device not in members:
                    report['devices'][group].update(state='running', detail=' + '.join(active))
        report['conditions'].append({'label': '공용 통로 주행 1대 · 팔2/팔3 동시 사용 금지', 'done': True})
        return report
