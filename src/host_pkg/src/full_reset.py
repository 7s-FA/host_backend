"""Exclusive, journaled initial-state workflow; never replay motion on restart."""
import json
from pathlib import Path
import uuid
from parallel_process import ParallelProcessController
from control import GROUPS
from initial_state import initial_steps


class FullResetController(ParallelProcessController):
    def __init__(self, *args, **kwargs):
        path = kwargs.get('state_file')
        saved = json.loads(Path(path).read_text()) if path and Path(path).exists() else {}
        self.full_reset = saved.get('full_reset')
        super().__init__(*args, **kwargs)
        if self.full_reset and self.full_reset['status'] == 'running':
            self.full_reset.update(status='failed', uncertain=bool(self.full_reset.get('task')),
                                   error='관제 재시작으로 초기화 중단 · 장치 결과 확인 필요. 자동 재실행 없음')
            self.note(self.full_reset['error']); self.save()

    def extra_state(self):
        return {**super().extra_state(), 'full_reset': self.full_reset}

    def steps(self):
        return initial_steps((self.full_reset or {}).get('amrs_parked', False))

    def reset_busy(self):
        r = self.full_reset or {}
        return r.get('status') == 'running' or bool(r.get('task') or r.get('uncertain') or r.get('stop_id'))

    def idle_available(self): return not self.reset_busy() and super().idle_available()
    def can_recover(self): return not self.reset_busy() and super().can_recover()
    def can_reset(self): return not self.reset_busy() and super().can_reset()
    def can_prepare_parked(self): return not self.reset_busy() and super().can_prepare_parked()
    def can_advance(self): return not self.reset_busy() and super().can_advance()

    def can_full_reset(self):
        return bool(not self.manual_inspection and not self.reset_busy() and self.link and all(self.ready.values())
                    and not self.active and not self.parallel_blocked() and not self.recovery_uncertain
                    and not self.recovery_stop and not self.stop_request and not self.reset_pending
                    and (not self.order or self.order['status'] in ('done', 'failed', 'paused', 'waiting')))

    def command(self, command):
        identity, action = command.get('id'), command.get('action')
        if not isinstance(identity, str) or not identity or identity in self.processed: return
        if action not in ('full_reset', 'cancel_full_reset'):
            incomplete = action == 'start' and (self.full_reset or {}).get('status') == 'failed'
            if not self.reset_busy() and not incomplete: return super().command(command)
            self.rejected.append(identity); self.processed.append(identity)
            self.note('전체 초기화 완료 전 새 주문 금지' if incomplete else '전체 초기화 종료·결과 확인 전 다른 지시 금지'); self.save(); return
        try:
            if action == 'cancel_full_reset':
                if not self.full_reset or self.full_reset['id'] != command.get('reset_id'):
                    raise ValueError('현재 전체 초기화와 일치하지 않습니다.')
                self.abort_full_reset('사용자 전체 초기화 중단')
            else:
                parked = command.get('amrs_parked', False)
                if type(parked) is not bool or (parked and self.mode != 'hardware'):
                    raise ValueError('지정 주차 위치 확인은 실물 모드에서만 사용할 수 있습니다.')
                if (not self.can_full_reset() or command.get('operator_confirmed') is not True
                    or command.get('order_id') != (self.order or {}).get('id')
                    or type(command.get('recovery_revision')) is not int
                    or command['recovery_revision'] != self.manual_revision):
                    raise ValueError('장치 정지·작업 종료·경로와 적재물 확인 또는 화면 갱신이 필요합니다.')
                self.manual_revision += 1
                self.full_reset = dict(id=uuid.uuid4().hex, status='running', step=0, task=None,
                                       uncertain=False, error='', stop_id=None, amrs_parked=parked)
                # Freeze an idle paused/waiting order; never run a production dependency.
                if self.order and self.order['status'] != 'done':
                    self.order.update(status='failed', pause_requested=False, fault='전체 초기화 진행 중')
                self.note('전체 초기화 시작 · 지정 주차 위치 확인 → M1/M2 위치·Nav2 준비 → 팔·리니어 복귀'
                          if parked else '전체 초기화 시작 · 팔 복귀 → 리니어 바깥쪽 → M1 주차 → M2 주차')
        except (ValueError, OSError) as exc:
            self.rejected.append(identity); self.note('전체 초기화 거절 · '+str(exc))
        self.processed.append(identity); self.save()

    def abort_full_reset(self, reason):
        r = self.full_reset
        if not r: return
        was_running = r['status'] == 'running'
        r.update(status='failed', error=reason)
        task = r.get('task')
        if task:
            r['uncertain'] = True
        self.note('전체 초기화 중단 · '+reason, task['device'] if task else None)
        self.save()
        if task and was_running and not task.get('preparation'):
            try:
                r['stop_id'] = self.transport.stop(task['device'])
                self.note('현재 장치 정지 요청 · 리니어는 목표까지 진행할 수 있음', task['device'])
            except Exception as exc: self.note('정지 응답 미확인 · '+str(exc))
            self.save()

    def fail(self, reason, uncertain=False, device=None):
        if self.reset_busy(): return self.abort_full_reset(reason)
        return super().fail(reason, uncertain=uncertain, device=device)

    def event(self, request_id, kind, data):
        r = self.full_reset or {}; task = r.get('task')
        if kind == 'stop' and r.get('stop_id') and r['stop_id'] == request_id:
            # A delayed stop must finish before a newly initialized job starts.
            # Goal rejection is also a final response: no stop job was created.
            # It does NOT prove the original motion stopped; keep its task until
            # that action has independently delivered a terminal Result.
            terminal = (data.get('status') in (4,5,6) or data.get('rejected') is True
                        or data.get('not_sent') is True)
            r['stop_result'] = dict(data)
            if not data.get('uncertain') and terminal:
                r['stop_id'] = None
                if not task: r['uncertain'] = False
            self.note('전체 초기화 정지 응답 · '+str(data.get('message'))+
                      (' · 원래 작업 결과 확인 필요' if task else
                       ' · 원래 작업 종료 확인, 재시도 가능' if terminal and not data.get('uncertain') else
                       ' · 정지 요청 결과 미확인'))
            self.save(); return
        if not task or request_id != task['id']:
            if kind == 'stop' and r.get('stop_id') == request_id:
                # Arm stop acknowledgements do not prove linear completion.
                self.note('전체 초기화 정지 응답 수신 · 원래 작업의 최종 결과 확인 필요'); self.save(); return
            return super().event(request_id, kind, data)
        if kind == 'accepted':
            task.update(accepted=True, accepted_at=self.clock())
            if r['status'] != 'running':
                try: r['stop_id'] = self.transport.stop(task['device'])
                except Exception as exc: self.note('늦은 접수 정지 요청 실패 · '+str(exc))
        elif kind == 'feedback':
            if data.get('message') in ('ERROR', 'PAUSED'):
                self.abort_full_reset(task['label']+' · '+data['message'])
        elif kind == 'done':
            if task.get('preparation'):
                data = dict(data, status=4 if data.get('success') is True else 6)
            if data.get('uncertain') or (task.get('accepted') and data.get('status') not in (4,5,6)):
                self.abort_full_reset(task['label']+' · 결과 미확인'); return
            success = task.get('accepted') and data.get('status') == 4 and data.get('success') is True and data.get('message') == 'IDLE'
            r.update(task=None, uncertain=bool(r.get('stop_id')))
            if r['status'] == 'running' and success:
                r['step'] += 1; self.note('전체 초기화 완료 단계 · '+task['label'], task['device'])
                if r['step'] == len(self.steps()):
                    try:
                        if self.order: self.finish_reset()
                        else:
                            self.clear_extra_state(); self.fault_device = None
                            self.manual_revision += 1
                        r.update(status='done', error='')
                        self.note('전체 초기 준비 완료 · 팔1·2·3 복귀, 리니어 바깥쪽, M1·M2 주차')
                    except OSError as exc: self.abort_full_reset('주문 기록 보관 실패 · '+str(exc))
            elif r['status'] == 'running':
                self.abort_full_reset(task['label']+' 실패 · '+str(data.get('message', 'ERROR')))
        self.save()

    def tick(self, link):
        if not self.reset_busy(): return super().tick(link)
        self.link, self.ready = link, self.transport.ready()
        r = self.full_reset
        if r['status'] != 'running': return
        task = r.get('task')
        # Parked preparation intentionally cycles localization/navigation. Keep
        # its reservation while Action discovery disappears during that restart.
        if not link or (not (task or {}).get('preparation') and not all(self.ready.values())):
            self.abort_full_reset('연결 끊김 · 다음 단계 실행 안 함'); return
        if task:
            deadline = task.get('accepted_at', task['submitted'])
            limit = task['timeout'] if task.get('accepted') else self.goal_timeout
            if self.clock()-deadline > limit: self.abort_full_reset(task['label']+' 응답 시간 초과')
            return
        device, command, label, timeout = self.steps()[r['step']]
        task = dict(id=uuid.uuid4().hex, device=device, command=command, label=label,
                    submitted=self.clock(), accepted=False, timeout=timeout)
        if command == 'PREPARE_PARKED':
            task.update(preparation=True, accepted=True, accepted_at=self.clock())
        r['task'] = task; self.save()  # Persist before any side effect.
        self.note('전체 초기화 · '+label, device)
        try:
            if task.get('preparation'): self.transport.prepare_parked(task.copy())
            else: self.transport.send(task.copy())
        except Exception as exc: self.abort_full_reset(label+' 전송 오류 · '+str(exc))

    def snapshot(self):
        report = super().snapshot(); r = self.full_reset
        report['supports_parked_full_reset'] = self.mode == 'hardware'
        report['can_full_reset'] = self.can_full_reset()
        report['full_reset'] = None if not r else {k:r[k] for k in ('id','status','step','uncertain','error')}
        if r:
            if r['status'] == 'failed':
                report['can_start'] = False
            steps = self.steps()
            label = steps[r['step']][2] if r['step'] < len(steps) else '전체 초기 준비 완료'
            report['full_reset'].update(label=label, total=len(steps), amrs_parked=r.get('amrs_parked',False))
            if self.reset_busy():
                for name in ('can_start','can_reset','can_retry','can_manual_move','can_prepare_parked','can_advance'):
                    report[name] = False
                for group, members in GROUPS.items():
                    if (r.get('task') or {}).get('device') in members:
                        report['devices'][group].update(state='running' if r['status']=='running' else 'unknown',detail=label)
            if r['status'] == 'failed' and not r.get('task'):
                device = steps[min(r['step'],len(steps)-1)][0]
                for group,members in GROUPS.items():
                    if device in members:
                        report['devices'][group].update(state='failed',detail=r['error'])
        return report
