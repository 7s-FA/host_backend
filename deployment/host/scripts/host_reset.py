#!/usr/bin/env python3
"""Operator-confirmed reset of a failed order through the local Host API."""
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = 'http://127.0.0.1:8082/api/live/'


def request(endpoint, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = Request(BASE + endpoint, data=body, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=5) as response:
        return json.load(response)


def main():
    if len(sys.argv) > 1:
        print('사용법: hostreset\n실패한 주문만 초기화합니다. 실행 중 현장 확인을 묻습니다.')
        return 0 if sys.argv[1] in ('-h', '--help') else 2
    state = request('state')
    if not state.get('bridge_connected'):
        print('Host 연결이 끊겨 주문 상태를 확인할 수 없습니다. hostrun과 연결 상태를 확인하세요.')
        return 1
    order = state.get('order')
    if not order:
        print('초기화할 주문이 없습니다.')
        return 0
    if order.get('status') != 'failed' or not state.get('can_reset'):
        print('초기화 불가: 실패 주문·장치 연결·이전 지시 응답을 먼저 확인하세요.')
        return 1
    identity = order['id']
    print('실패 주문:', identity)
    print('모든 로봇과 리니어가 멈추고 작업이 끝났으며, 초기 배치와 자재 상태를 확인하세요.')
    print('실패 기록을 보관합니다. 필요한 정지 확인 외에 이동·정지 잠금 해제·좌표 설정은 하지 않습니다.')
    if input('확인했다면 "초기화" 입력 (그 외 취소): ').strip() != '초기화':
        print('취소했습니다.')
        return 0
    request('reset', {'order_id': identity, 'operator_confirmed': True})
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        state = request('state')
        if state.get('bridge_connected'):
            current = state.get('order')
            if current is None:
                print('초기화 완료. 실패 기록은 .runtime/host/order-history/에 보관했습니다.')
                print('실물 시험 전 hostready로 준비하고, 웹에서 1개·수동 진행으로 시작하세요.')
                return 0
            if current['id'] != identity:
                print('다른 주문으로 변경되었습니다. 웹 상태를 확인하세요.')
                return 1
            if not state.get('pending_commands') and not state.get('reset_pending'):
                print('초기화 보류:', state.get('latest_event', 'Host 로그 확인 필요'))
                return 1
        time.sleep(0.5)
    print('초기화 결과 미확인. 재실행 전 웹의 주문 상태와 Host 로그를 확인하세요.')
    return 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except HTTPError as exc:
        try:
            detail = json.load(exc).get('error', str(exc))
        except (ValueError, AttributeError):
            detail = str(exc)
        print('초기화 거절:', detail, file=sys.stderr)
        raise SystemExit(1)
    except (URLError, TimeoutError, OSError, EOFError) as exc:
        print('관제 연결 또는 입력 확인 필요:', exc, file=sys.stderr)
        raise SystemExit(1)
