#!/usr/bin/env python3
"""Stop this workspace's ROS launch gracefully, without stopping robot servers."""
import argparse
import os
from pathlib import Path
import select
import signal
import sys

ROOT = Path(__file__).resolve().parents[1]
ROS2 = '/opt/ros/jazzy/bin/ros2'
LAUNCH = str(ROOT / 'host_web/host/host_control.launch.py')


def matches(argv):
    return len(argv) >= 4 and argv[1:4] == [ROS2, 'launch', LAUNCH]


def find_launches():
    found = []
    for folder in Path('/proc').iterdir():
        if not folder.name.isdigit():
            continue
        descriptor = None
        try:
            if folder.stat().st_uid != os.getuid():
                continue
            descriptor = os.pidfd_open(int(folder.name))
            argv = folder.joinpath('cmdline').read_bytes().decode().rstrip('\0').split('\0')
            if matches(argv):
                found.append((int(folder.name), descriptor))
                descriptor = None
        except (OSError, UnicodeError):
            pass
        finally:
            if descriptor is not None:
                os.close(descriptor)
    return found


def stop(found, timeout=25):
    poller = select.poll()
    pending = set()
    for pid, descriptor in found:
        try:
            signal.pidfd_send_signal(descriptor, signal.SIGINT)
        except ProcessLookupError:
            continue
        poller.register(descriptor, select.POLLIN)
        pending.add(descriptor)
        print(f'관제 정상 종료 요청: PID {pid}', flush=True)
    import time
    deadline = time.monotonic() + timeout
    while pending and time.monotonic() < deadline:
        for descriptor, _ in poller.poll(min(500, max(0, int((deadline-time.monotonic())*1000)))):
            pending.discard(descriptor)
            poller.unregister(descriptor)
    if pending:
        raise RuntimeError('종료 응답 시간 초과. 기존 hostrun 터미널을 확인하세요. 강제 종료는 하지 않았습니다.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='대상 확인만 수행; 종료하지 않음')
    args = parser.parse_args()
    found = find_launches()
    try:
        if not found:
            print('실행 중인 관제 서버가 없습니다. 초기 위치 준비 중이면 해당 hostrun 터미널에서 Ctrl+C를 누르세요.')
            return
        if args.check:
            print('관제 종료 대상 PID: ' + ', '.join(str(pid) for pid, _ in found))
            return
        print('관제 웹·ROS 연결·백엔드를 종료합니다. 로봇 서버 종료나 비상정지 명령은 아닙니다.', flush=True)
        stop(found)
        print('관제 종료 완료. 다시 켜기: hostrun')
    finally:
        for _, descriptor in found:
            os.close(descriptor)


if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
