#!/usr/bin/env python3
"""HTTP -> controller -> real ROS Action transport -> mock devices, Domain 149 only."""
from contextlib import contextmanager
from collections import Counter
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'host_backend/src/host_pkg/src'))
from parallel_process import make_parallel_plan
OPENER = build_opener(ProxyHandler({}))
BASE = 'http://127.0.0.1:8082'
EVENTS = ROOT / '.runtime/host/mock-events.jsonl'


def api(path, body=None):
    request = Request(BASE + '/api/live/' + path, None if body is None else json.dumps(body).encode(),
                      {'Content-Type': 'application/json', 'Origin': BASE})
    with OPENER.open(request, timeout=2) as response:
        return json.load(response)


def until(predicate, seconds=45):
    deadline = time.monotonic() + seconds
    last = None
    while time.monotonic() < deadline:
        try:
            last = api('state')
            if predicate(last):
                return last
        except (OSError, ValueError):
            pass
        time.sleep(.05)
    raise AssertionError(f'Timed out; last state={last}')


def events():
    return [json.loads(line) for line in EVENTS.read_text().splitlines()]


def accepted_since(offset):
    return [(item['device'], item['command']) for item in events()[offset:] if item['event'] == 'accepted' and item['command'] != 'EMER_STOP']


@contextmanager
def stack(name, fault='', delay='.35', timeout='20'):
    with tempfile.TemporaryDirectory(prefix='host-process-test-') as temporary:
        env = dict(os.environ, HOST_MOCK_DELAY=delay, HOST_MOCK_FAULT=fault,
                   HOST_STATE_FILE=str(Path(temporary) / 'order.json'), HOST_ARM_TIMEOUT=timeout)
        log_path = ROOT / '.runtime/host' / f'process-{name}.log'
        with log_path.open('w') as stream:
            process = subprocess.Popen(['bash', str(ROOT / 'start_host.sh'), '--mock'], env=env,
                                       cwd='/tmp', stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                state = until(lambda s: s['bridge_connected'] and s.get('can_start'), seconds=25)
                assert state['runtime_mode'] == 'mock'
                assert process.poll() is None, log_path.read_text()
                yield
            except Exception:
                print(log_path.read_text()[-8000:], file=sys.stderr)
                raise
            finally:
                if process.poll() is None:
                    process.send_signal(signal.SIGINT)
                    try:
                        process.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=5)
                assert process.returncode == 0, log_path.read_text()


def completed():
    result = until(lambda s: not s['pending_commands'] and (s.get('order') or {}).get('status') in ('done', 'failed'))
    assert result['order']['status'] == 'done', result
    return result['order']


def main():
    with stack('success'):
        for product in ('A', 'B'):
            for quantity in (1, 2):
                offset = len(events())
                api('start', {'product_type': product, 'quantity': quantity})
                order = completed()
                assert (order['completed'], order['product_remaining'], order['transport_remaining']) == (quantity, 0, 0)
                expected = [(step.device, step.command) for step in make_parallel_plan(product, quantity) if step.device != 'arm3']
                assert Counter(accepted_since(offset)) == Counter(expected), accepted_since(offset)
                print(f'PASS HTTP/ROS {product} x {quantity}: {len(expected)} dependency-gated successful actions', flush=True)
        offset = len(events())
        api('start', {'product_type': 'A', 'quantity': 1, 'auto_advance': False})
        until(lambda s: (s.get('order') or {}).get('status') == 'waiting')
        time.sleep(.6)
        assert len(accepted_since(offset)) == 2  # M1 travel and initial linear preparation
        state = api('state')
        while state['order']['status'] != 'done':
            stage = state['order']['stage']
            api('next', {})
            state = until(lambda s: (s.get('order') or {}).get('stage', 0) > stage and s['order']['status'] in ('waiting', 'done'))
        assert state['order']['status'] == 'done'
        print('PASS manual: waits at every Result; next advances once', flush=True)
        offset = len(events())
        api('start', {'product_type': 'B', 'quantity': 2})
        until(lambda s: (s.get('order') or {}).get('status') == 'running' and not s['pending_commands'])
        api('pause', {})
        until(lambda s: (s.get('order') or {}).get('status') == 'paused' and not s['pending_commands'])
        paused = len(accepted_since(offset))
        time.sleep(.6)
        assert len(accepted_since(offset)) == paused
        api('resume', {})
        completed()
        assert Counter(accepted_since(offset)) == Counter((step.device, step.command) for step in make_parallel_plan('B', 2) if step.device != 'arm3')
        print('PASS pause/resume: current Result finishes, no duplicated actions', flush=True)
    for fault in ('reject', 'error', 'stall'):
        with stack(f'chain-{fault}', f'arm2:BUILD_LOAD_A:{fault}', delay='.2', timeout='1' if fault == 'stall' else '20'):
            api('start', {'product_type': 'A', 'quantity': 1})
            state = until(lambda s: (s.get('order') or {}).get('status') == 'failed')
            assert state['order']['completed'] == 0
            # Departure may already be running alongside arm3; it must not count as product completion.
            assert state['order']['product_remaining'] == 1
            if fault == 'stall':
                deadline = time.monotonic() + 5
                while not any(e['command'] == 'EMER_STOP' for e in events()) and time.monotonic() < deadline:
                    time.sleep(.05)
                assert any(e['command'] == 'EMER_STOP' for e in events())
            time.sleep(.5)
            assert api('state')['order']['status'] == 'failed'
            print(f'PASS BUILD_LOAD {fault}: no completed count, failure retained; outstanding work stopped', flush=True)
    print('PASS complete: only localhost Domain 149 mock devices were used', flush=True)


if __name__ == '__main__': main()
