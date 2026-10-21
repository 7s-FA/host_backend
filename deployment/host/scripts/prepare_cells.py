#!/usr/bin/env python3
"""Prepare arms through exclusive actions before starting the Host order server."""
import math
import json
import os
from pathlib import Path
import subprocess
import signal
import sys
import time
import uuid

from startup_action import await_reply, release_once

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'host_backend/src/host_pkg/src'))
from initial_state import RELEASE_STEPS, HOME_STEPS, StartupJournal
PEERS=(('warehouse','warehouse@192.0.2.166'),('workcell','robot@192.0.2.113'))


def unresolved(saved):
    order=saved.get('order')
    parallel=saved.get('parallel_state',{})
    return bool((order and order.get('status') not in ('done','completed')) or saved.get('active') or
                saved.get('recovery_uncertain') or saved.get('reset_stop_device') or
                (saved.get('full_reset') or {}).get('status')=='running' or
                (saved.get('full_reset') or {}).get('uncertain') or (saved.get('full_reset') or {}).get('task') or
                any(parallel.get(k) for k in ('inflight','orphans','parallel_stops','pending_stops','unconfirmed')))


def release_latches(send):
    for device,command,label,timeout in RELEASE_STEPS:
        send('/'+device+'/data',command,timeout)


def prepare(send,verify):
    release_latches(send)
    verify()
    for device,command,label,timeout in HOME_STEPS:
        send('/'+device+'/data',command,timeout)


def cleanup_only(send, verify, report=print):
    """Clear stopped jobs independently; never send home, resume or drive goals."""
    failures=[]
    for device,command,label,timeout in RELEASE_STEPS:
        try:
            send('/'+device+'/data',command,timeout)
            report('[OK] '+label)
        except Exception as exc:
            failures.append(label+': '+str(exc))
            report('[미완료] '+failures[-1])
    try: verify()
    except Exception as exc: failures.append('장치 정리 후 확인: '+str(exc))
    if failures:
        raise RuntimeError('전체 정리 미완료\n'+'\n'.join(failures))
    report('전체 작업 정리 완료. 다음: hostrun (센서·모터·초기 자세 준비 후 웹 실행)')


def prepare_amrs():
    # RESTART only clears a latch. Check live sensor/TF feedback and enable
    # torque through the existing no-goal worker, without reseeding parking.
    print('M1·M2 센서·모터 토크 준비 확인 (주차 좌표 변경 없음)',flush=True)
    subprocess.run(['/bin/bash',str(ROOT/'start_amr.sh'),'--ready'],
                   check=True,timeout=660)


def main(*, cleanup=False):
    if os.environ.get('ROS_DOMAIN_ID')!='40' or os.environ.get('HOST_MOCK')=='1':
        raise RuntimeError('실물 Domain 40 전용입니다. 모의 실행에서는 호출하지 마세요.')
    path=Path(os.environ.get('HOST_STATE_FILE',str(ROOT/'.runtime/host/order-hardware.json')))
    saved=json.loads(path.read_text()) if path.exists() else {}
    if cleanup:
        if unresolved(saved) or saved.get('recovery_stop') or saved.get('stop_request') or saved.get('reset_pending') or (saved.get('full_reset') or {}).get('stop_id'):
            raise RuntimeError('미정리 주문/응답 미확인 작업이 있습니다. hostrun --no-arm-prepare로 웹을 열어 중단·결과 확인·실패 주문 초기화를 먼저 진행하세요. 기록은 유지합니다.')
        print('팔1·팔2/3 중단 작업 정리 및 리니어 정지 확인, M1/M2 정지 잠금 해제',flush=True)
        print('모든 장치가 실제로 멈췄고 공정이 끝났을 때만 실행하세요. 원점 복귀·주차 이동·리니어 이동·팔 작업 재개는 요청하지 않습니다.',flush=True)
        if input('확인했다면 "정리" 입력 (그 외 취소): ').strip() != '정리':
            print('취소했습니다.');return
    journal=StartupJournal(path,saved)
    helper=(ROOT/'scripts/cell_remote.py').read_text()
    def remote(kind,peer):
        print(f'[{kind}] 서버·준비 조건 확인: {peer}',flush=True)
        subprocess.run(['ssh','-T','-o','BatchMode=yes','-o','ConnectTimeout=8',
                        '-o','ServerAliveInterval=5','-o','ServerAliveCountMax=3',peer,
                        'python3 - '+kind],input=helper,text=True,check=True,timeout=40)
    if unresolved(saved):
        # Starting the warehouse listener permits error recovery; no HOME goal
        # is sent while any persisted order or movement is unresolved.
        try:remote(*PEERS[0])
        except (OSError,subprocess.SubprocessError) as exc:print('자재창고 연결 확인 필요: '+str(exc),flush=True)
        print('미정리 주문/작업 기록: 팔·리니어 준비 이동을 생략하고 복구용 관제를 엽니다.',flush=True)
        print('기록 정리 후 관제를 종료하고 hostrun을 다시 실행하세요.',flush=True)
        return
    for kind,peer in PEERS:
        remote('workcell-start' if kind=='workcell' else kind,peer)
    import rclpy
    from rclpy.action import ActionClient
    from rclpy.signals import SignalHandlerOptions
    from host_pkg.action import Arm,Burger
    from std_msgs.msg import String
    from unique_identifier_msgs.msg import UUID
    # Keep ROS alive long enough to request HOLD when this terminal is stopped.
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    def interrupted(*_):raise KeyboardInterrupt('사용자 중단')
    signal.signal(signal.SIGINT,interrupted);signal.signal(signal.SIGTERM,interrupted)
    node=rclpy.create_node('host_startup_preparation')
    types={name:Arm for name in ('/arm1/data','/arm2/data')}
    types.update({name:Burger for name in ('/M1/data','/M2/data')})
    clients={name:ActionClient(node,action,name) for name,action in types.items()}
    result_clients={name:node.create_client(action.Impl.GetResultService,name+'/_action/get_result')
                    for name,action in types.items()}
    status={}
    def receive(msg):
        try:status.update(value=json.loads(msg.data),at=time.monotonic())
        except ValueError:pass
    subscription=node.create_subscription(String,'/arm1/status',receive,10)
    def wait(future,seconds,label='시작 준비'):
        return await_reply(node,rclpy,future,seconds,label)
    def query_result(name,goal_id,seconds):
        request=types[name].Impl.GetResultService.Request()
        request.goal_id=goal_id
        client=result_clients[name]
        future=client.call_async(request)
        try:return wait(future,seconds,name+' 최종 결과 조회')
        finally:
            if not future.done():client.remove_pending_request(future)
    def send(name,command,timeout):
        print(f'시작 준비: {name} {command}',flush=True)
        goal=types[name].Goal();goal.command=command
        if name in ('/M1/data','/M2/data'):
            speed=float(os.environ.get('HOST_SPEED_PERCENT','100'))
            if not math.isfinite(speed) or not 0<speed<=100:raise ValueError('이동 속도 설정 확인 필요')
            goal.cmd_val=speed if command=='GO_TO_PARK' else 0.
        if command in ('CLEAR_ERROR','RESTART'):
            release_once(clients[name],goal,UUID(uuid=list(uuid.uuid4().bytes)),wait,
                         lambda goal_id,seconds:query_result(name,goal_id,seconds),
                         timeout,name+' '+command)
            print(command+': 준비 완료',flush=True)
            return
        handle=None
        terminal=False
        request_id=journal.begin(name.split('/')[1],command)
        try:
            handle=wait(clients[name].send_goal_async(goal,goal_uuid=UUID(uuid=list(uuid.UUID(hex=request_id).bytes))),8,name+' '+command+' 접수')
            if not handle.accepted:
                terminal=True
                raise RuntimeError(command+': 거절 · 실행 중 작업/서버 버전 확인')
            journal.accepted()
            result=wait(handle.get_result_async(),timeout,name+' '+command+' 완료')
            terminal=result.status in (4,5,6)
            if result.status!=4 or not result.result.success or result.result.message!='IDLE':
                raise RuntimeError(name+' '+command+': 실패 · '+str(result.result.message))
            journal.result(True)
        except BaseException as exc:
            journal.result(False,uncertain=not terminal,error=str(exc))
            # Do not retry/resume. Request arm HOLD on timeout/interruption.
            if not terminal and command in ('HOME_A','RESET','BUILD_SLIDE','GO_TO_PARK') and (handle is None or handle.accepted):
                stop=types[name].Goal();stop.command='EMER_STOP'
                try:
                    stopped=wait(clients[name].send_goal_async(stop),3)
                    if not stopped.accepted:raise RuntimeError('정지 요청 거절')
                    reply=wait(stopped.get_result_async(),20)
                    if reply.status!=4 or not reply.result.success:raise RuntimeError('정지 실패')
                    print('장치 정지 응답 확인 · 리니어는 기존 목표까지 진행할 수 있습니다.',flush=True)
                except BaseException:print('정지 결과 미확인 · 실제 장치 상태를 확인하세요.',file=sys.stderr)
            raise
        print(command+': 준비 완료',flush=True)
    def check_arm1(*,cleared):
        # Require a newly received report after cleanup, not the cached PAUSED.
        after=time.monotonic()
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            rclpy.spin_once(node,timeout_sec=.1)
            value=status.get('value',{})
            if status.get('at',0)>after and value.get('supports_home') and value.get('supports_error_reset'):
                allowed=('IDLE',) if cleared else ('IDLE','PAUSED','ERROR')
                if (value.get('mock') is not False or value.get('state') not in allowed or
                        (value.get('state')=='IDLE' and value.get('command'))):
                    raise RuntimeError('팔1이 작업 중이거나 정리되지 않았습니다. 시작 준비 중단')
                return
        else:raise RuntimeError('팔1 시작 자세 기능 응답 없음 · 서버 업데이트/재실행 필요')
    def verify():
        check_arm1(cleared=True)
        remote(*PEERS[1])
        prepare_amrs()
    try:
        for name,client in clients.items():
            if not client.wait_for_server(timeout_sec=120):raise RuntimeError(name+': 서버 연결 실패 · M1/M2는 hostamr 실행 확인')
        # Discovery alone does not prove that service responses reach this PC.
        # Query an unknown goal before modifying any latch; this sends no goal.
        for name in clients:
            reply=query_result(name,UUID(uuid=list(uuid.uuid4().bytes)),8)
            if reply.status!=0:raise RuntimeError(name+': 통신 점검용 목표 ID 응답 불일치')
            print(name+': 응답 왕복 확인',flush=True)
        if cleanup:
            def verify_cleanup():
                check_arm1(cleared=True)
                remote(*PEERS[1])
            cleanup_only(send,verify_cleanup)
            return
        check_arm1(cleared=False)
        prepare(send,verify)
        print('M1·M2 정지 잠금 해제 + 팔1·2·3 시작 자세 + 리니어 바깥쪽 + M1·M2 지정 주차 준비 완료. 웹에서 주문을 시작하세요.',flush=True)
    finally:
        node.destroy_subscription(subscription)
        for client in clients.values():client.destroy()
        for client in result_clients.values():node.destroy_client(client)
        node.destroy_node();rclpy.try_shutdown()


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleanup-only',action='store_true',help='정지한 장치의 작업·잠금만 정리; 이동 없음')
    args=parser.parse_args()
    try:main(cleanup=args.cleanup_only)
    except (Exception,KeyboardInterrupt) as exc:
        print('시작 준비 중단: '+str(exc),file=sys.stderr)
        print('상태 확인용 웹만 열기: hostrun --no-arm-prepare',file=sys.stderr)
        raise SystemExit(1)
