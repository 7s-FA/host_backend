"""SSH startup helper; starts control servers only, never sends a robot goal."""
import fcntl
import os
from pathlib import Path
import subprocess
import sys
import time


def run(*args):
    return subprocess.run(args,check=True,text=True,capture_output=True).stdout.strip()


def stale_server_modules(app,started):
    # Only modules retained by the long-lived action server need its restart.
    # run_episode.sh execs a fresh Python -B episode_cli.py for every job;
    # episode_recovery is loaded by that child, not by the action server.
    return [name for name in ('action_server.py','action_protocol.py','linear_client.py','network_ready.py')
            if (app/name).stat().st_mtime>started]


def main(kind):
    if kind=='warehouse':
        root=Path('/home/warehouse/Downloads/so101_imitation')
        app=root/'integration/arm1'
        if "'HOME_A'" not in (app/'engine.py').read_text():
            raise RuntimeError('자재창고 서버에 HOME_A 업데이트가 필요합니다.')
        # An existing terminal server owns this same lock. Preserve it.
        with (app/'hardware.lock').open('a') as lock:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:
                print('자재창고: 실행 중인 서버 유지');return
        unit='warehouse-arm1.service'
        state=run('systemctl','--user','show',unit,'-p','ActiveState','--value')
        if state not in ('active','activating'):
            if state=='failed':run('systemctl','--user','reset-failed',unit)
            run('systemd-run','--user','--collect','--unit='+unit,
                '--working-directory='+str(root),'/bin/bash',str(root/'run-arm1-server.sh'))
        print('자재창고: 서버 시작 요청 완료 · 초기 자세 명령은 관제에서 별도 전송')
    elif kind in ('workcell','workcell-start'):
        root=Path('/home/robot/OpenCV_teach')
        app=root/'integration'
        if "'PREPARE_HOME'" not in (app/'action_server.py').read_text():
            raise RuntimeError('조립대 서버에 PREPARE_HOME 업데이트가 필요합니다.')
        for unit in ('arm3-linear-controller.service','workcell-actions.service'):
            state=run('systemctl','show',unit,'-p','ActiveState','--value')
            if state!='active':
                try:run('sudo','-n','systemctl','start',unit)
                except subprocess.CalledProcessError:
                    raise RuntimeError('조립대 PC에서 관리자 실행 필요: sudo systemctl start '+unit) from None
        stamp=int(run('systemctl','show','workcell-actions.service','-p','ExecMainStartTimestampMonotonic','--value'))/1e6
        started=time.time()-time.monotonic()+stamp
        stale=stale_server_modules(app,started)
        if stale:
            raise RuntimeError('조립대 상주 코드 변경 ('+', '.join(stale)+
                               '): sudo systemctl restart workcell-actions.service')
        if kind=='workcell-start':
            # A paused CLI owns the lock until CLEAR_ERROR has safely ended it.
            # The action server validates linear stop and rejects running jobs.
            print('조립대: 서버 확인 완료 · 중단 작업 정리는 CLEAR_ERROR로 확인')
            return
        with (root/'data/episode-cli.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            os.chdir(root);sys.path[:0]=[str(root),str(app)]
            import episode_cli,episode_recovery
            from linear_client import LinearClient
            episode_recovery.workcell_records(episode_cli)
            stage=LinearClient().call('status')
            if stage.get('phase')!='TIMED_COMPLETE' or stage.get('owned'):
                raise RuntimeError('리니어 정지·사용권 확인 필요: '+str(stage.get('phase')))
        print('조립대: 서버·팔2/3 저장 자세·리니어 정지 확인 완료')
    else:raise ValueError('unknown cell')


if __name__=='__main__':
    try:main(sys.argv[1])
    except Exception as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(1)
