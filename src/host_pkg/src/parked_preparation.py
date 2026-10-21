"""Run the existing single-robot readiness CLI without blocking ROS callbacks."""
import os
from pathlib import Path
import subprocess
import threading


def execute(task, events, *, runner=subprocess.run, root=None):
    root = Path(root) if root else Path(__file__).resolve().parents[4]
    started = False
    try:
        options = dict(stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, env=dict(os.environ, HOST_AMR_BATCH='1'))
        probe = runner(['bash', str(root / 'start_amr.sh'), '--status', '--robot', task['device']],
                       timeout=25, **options)
        if probe.returncode:
            events.put((task['id'], 'done', dict(success=False, uncertain=False,
                        message='SSH·서버 상태 확인 실패 · 준비 실행 없음: '+probe.stdout[-1200:])))
            return
        started = True
        result = runner(
            ['bash', str(root / 'start_amr.sh'), '--ready', '--parked', '--robot', task['device']],
            timeout=600, **options)
        success = result.returncode == 0
        # The remote may continue after a failed SSH/request. Only a successful
        # readiness result releases this reservation automatically.
        data = dict(success=success, uncertain=not success,
                    message='IDLE' if success else result.stdout[-1800:])
    except (OSError, subprocess.TimeoutExpired) as exc:
        data = dict(success=False, uncertain=started, message=str(exc))
    events.put((task['id'], 'done', data))


def start(task, events):
    if task.get('device') not in ('M1', 'M2') or os.environ.get('HOST_MOCK') == '1':
        raise ValueError('실물 M1/M2 주차 준비만 지원합니다.')
    threading.Thread(target=execute, args=(task.copy(), events),
                     name='parked-preparation', daemon=True).start()
