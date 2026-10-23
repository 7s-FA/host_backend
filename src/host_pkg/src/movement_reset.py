"""Explicit AMR job cleanup: confirmed stop, then release; never change pose."""
import json
from pathlib import Path
import uuid
from full_reset import FullResetController


class MovementResetController(FullResetController):
    def __init__(self, *args, **kwargs):
        path = kwargs.get('state_file')
        saved = json.loads(Path(path).read_text()) if path and Path(path).exists() else {}
        super().__init__(*args, **kwargs)
        task = saved.get('active') or {}
        if task.get('movement_reset'):
            self.active = dict(task, failed=True)
            self.recovery_stop = None
            self.recovery_uncertain = True
            self.save()

    def can_reset_movement(self, device):
        task = self.active or self.recovery_stop
        return bool(device in ('M1', 'M2') and self.link and self.ready.get(device)
                    and not self.reset_busy() and not self.parallel_blocked()
                    and not self.stop_request and not self.reset_pending
                    and (not self.order or self.order['status'] in ('done', 'failed'))
                    and (not task or (task.get('manual') and task.get('failed')
                         and not task.get('preparation') and task.get('device') == device))
                    and self.reset_stop_device in (None, device))

    def command(self, command):
        if command.get('action') != 'reset_movement':
            return super().command(command)
        identity = command.get('id')
        if not isinstance(identity, str) or not identity or identity in self.processed:
            return
        device = command.get('device')
        if (not self.can_reset_movement(device) or command.get('operator_confirmed') is not True
                or command.get('order_id') != (self.order or {}).get('id')
                or type(command.get('recovery_revision')) is not int
                or command['recovery_revision'] != self.manual_revision):
            self.rejected.append(identity)
            self.note('이동 초기화 거절 · 작업 종료·현재 화면·선택 로봇 연결 확인 필요')
        else:
            previous = self.active or self.recovery_stop
            # Keep the interrupted job in the journal until both responses arrive.
            self.active = dict(id=uuid.uuid4().hex, device=device, manual=True,
                               movement_reset=True, command='EMER_STOP',
                               label=device+' 이동 초기화 · 정지 확인', phase='stop',
                               submitted=self.clock(), interrupted=previous)
            self.recovery_stop = None
            self.recovery_uncertain = True
            self.manual_revision += 1
            if self.order:
                self.order['recovery_revision'] = self.order.get('recovery_revision', 0) + 1
            self.save()
            try:
                self.active['stop_id'] = self.transport.stop(device)
            except Exception as exc:
                self.active['failed'] = True
                self.note('이동 초기화 정지 요청 실패 · '+str(exc), device)
        self.processed.append(identity)
        self.save()

    def event(self, request_id, kind, data):
        task = self.active or {}
        if not task.get('movement_reset'):
            return super().event(request_id, kind, data)
        expected = task.get('stop_id') if task['phase'] == 'stop' else task['id']
        if request_id != expected or task.get('failed'):
            return
        if kind != ('stop' if task['phase'] == 'stop' else 'done'):
            return
        if not (data.get('success') is True and data.get('status') == 4 and data.get('message') == 'IDLE'):
            task['failed'] = True
            self.note('이동 초기화 실패 · '+str(data.get('message')), task['device'])
        elif task['phase'] == 'stop':
            task.update(id=uuid.uuid4().hex, phase='release', command='RESTART',
                        label=task['device']+' 이동 초기화 · 잠금 해제', submitted=self.clock())
            self.save()
            try:
                self.transport.send(task.copy())
            except Exception as exc:
                task['failed'] = True
                self.note('이동 초기화 잠금 해제 요청 실패 · '+str(exc), task['device'])
        else:
            self.note('이동 초기화 완료 · 남은 작업 해제 · 위치 좌표 유지 · 자동 이동 없음', task['device'])
            self.active = self.recovery_stop = self.reset_stop_device = None
            self.recovery_uncertain = False
        self.save()

    def tick(self, link):
        if not (self.active or {}).get('movement_reset'):
            return super().tick(link)
        self.link, self.ready = link, self.transport.ready()
        if not self.active.get('failed') and self.clock() - self.active['submitted'] > 15:
            self.active['failed'] = True
            self.note('이동 초기화 응답 시간 초과 · 결과 미확인, 자동 이동 금지', self.active['device'])
            self.save()

    def snapshot(self):
        report = super().snapshot()
        report['movement_reset_available'] = {d: self.can_reset_movement(d) for d in ('M1', 'M2')}
        return report
