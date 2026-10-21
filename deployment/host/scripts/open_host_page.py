#!/usr/bin/env python3
"""Open the operator page after the expected local Host is ready (GET only)."""
import argparse
import json
import os
import shutil
import subprocess
import time
from urllib.request import ProxyHandler, build_opener

PAGE_URL = 'http://localhost:8082/control.html'
STATE_URL = 'http://127.0.0.1:8082/api/live/state'


def open_page(mode, timeout=30, parent_pid=None, manual=False):
    browser = shutil.which('xdg-open')
    if not browser or not (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
        print(f'브라우저를 자동으로 열 수 없습니다. 직접 열어주세요: {PAGE_URL}', flush=True)
        return 1
    opener = build_opener(ProxyHandler({}))
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if parent_pid is not None:
            try:
                os.kill(parent_pid, 0)
            except ProcessLookupError:
                return 1
        try:
            with opener.open(STATE_URL, timeout=1) as response:
                state = json.load(response)
            ready = isinstance(state, dict) and state.get('mode') == 'live' and (
                state.get('bridge_configured') is False if mode == 'monitor' else
                state.get('bridge_connected') is True and state.get('runtime_mode') == mode
            )
            if ready and mode != 'monitor':
                ready = bool(state.get('manual_inspection')) == manual
            if ready:
                break
        except (OSError, ValueError):
            pass
        time.sleep(0.25)
    else:
        print(f'관제 준비를 확인하지 못했습니다. 터미널 로그를 확인하고 직접 열어주세요: {PAGE_URL}', flush=True)
        return 1

    # The browser must not inherit ROS libraries, the bridge token, or the Host lock.
    environment = dict(os.environ)
    for key in ('ROBOT3_BRIDGE_TOKEN', 'LD_LIBRARY_PATH', 'PYTHONPATH', 'PYTHONHOME'):
        environment.pop(key, None)
    try:
        process = subprocess.Popen([browser, PAGE_URL], env=environment, close_fds=True,
                                   start_new_session=True, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            if process.wait(timeout=5) != 0:
                raise OSError('xdg-open failed')
        except subprocess.TimeoutExpired:
            pass  # Some desktop openers stay attached to the browser.
    except OSError:
        print(f'브라우저 열기에 실패했습니다. 직접 열어주세요: {PAGE_URL}', flush=True)
        return 1
    print(f'관제 웹화면 열기: {PAGE_URL}', flush=True)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('hardware', 'mock', 'monitor'), required=True)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--parent-pid', type=int)
    parser.add_argument('--manual', action='store_true')
    args = parser.parse_args()
    raise SystemExit(open_page(args.mode, args.timeout, args.parent_pid, args.manual))
