#!/usr/bin/env python3
"""Exercise startup/shutdown in localhost-only Domain 149; never publish commands."""
import asyncio
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
from urllib.request import urlopen

from tornado.websocket import websocket_connect

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime/host'
ENV = dict(os.environ, HOST_ROS_DOMAIN_ID='149', HOST_DISCOVERY_RANGE='LOCALHOST',
           HOST_OPEN_BROWSER='0')


def assert_ports_free():
    for port in (8082, 9090):
        with socket.socket() as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            probe.bind(('127.0.0.1', port))


def descendants(pid):
    try:
        children = Path(f'/proc/{pid}/task/{pid}/children').read_text().split()
    except FileNotFoundError:
        return []
    result = []
    for child in children:
        result.append(int(child))
        result.extend(descendants(int(child)))
    return result


async def verify_ros(with_backend):
    connection = await websocket_connect('ws://127.0.0.1:9090', connect_timeout=3)
    try:
        await connection.write_message(json.dumps({
            'op': 'call_service', 'service': '/rosapi/nodes', 'id': 'startup-check',
        }))
        while True:
            raw = await asyncio.wait_for(connection.read_message(), timeout=8)
            assert raw is not None, 'rosbridge disconnected'
            message = json.loads(raw)
            if message.get('id') == 'startup-check':
                assert message.get('result'), message
                nodes = message['values']['nodes']
                assert ('/control' in nodes) == with_backend, nodes
                break
        if with_backend:
            await connection.write_message(json.dumps({
                'op': 'subscribe', 'topic': '/ros_to_web',
                'type': 'std_msgs/msg/String',
            }))
            while True:
                raw = await asyncio.wait_for(connection.read_message(), timeout=8)
                assert raw is not None, 'rosbridge disconnected'
                message = json.loads(raw)
                if message.get('op') == 'publish' and message.get('topic') == '/ros_to_web':
                    status = json.loads(message['msg']['data'])
                    assert 'host_mode' in status and 'order' in status
                    break
    finally:
        connection.close()


async def run_case(with_backend):
    name = 'full' if with_backend else 'monitor'
    log_path = RUNTIME / f'smoke-{name}.log'
    command = ['bash', str(ROOT / 'start_host.sh')]
    if not with_backend:
        command.append('--monitor-only')
    with log_path.open('w') as log:
        process = subprocess.Popen(command, cwd='/tmp', env=ENV, stdout=log,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        try:
            deadline = time.monotonic() + 30
            while True:
                assert process.poll() is None, log_path.read_text()
                try:
                    with urlopen('http://127.0.0.1:8082/?live=1', timeout=1) as response:
                        assert response.status == 200
                    with socket.create_connection(('127.0.0.1', 9090), timeout=1):
                        pass
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise AssertionError(log_path.read_text())
                    await asyncio.sleep(0.2)
            # Let DDS discover the freshly started local nodes before querying rosapi.
            await asyncio.sleep(2)
            await verify_ros(with_backend)
            duplicate = subprocess.run(command, cwd='/tmp', env=ENV, capture_output=True,
                                       text=True, timeout=15)
            assert duplicate.returncode == 1 and '이미 관제' in duplicate.stderr, duplicate
            if with_backend:
                process.send_signal(signal.SIGINT)
                assert process.wait(timeout=20) == 0, log_path.read_text()
                assert 'Traceback' not in log_path.read_text(), log_path.read_text()
            else:
                # Fail only a process created by this test; verify sibling cleanup.
                for child in descendants(process.pid):
                    try:
                        arguments = Path(f'/proc/{child}/cmdline').read_bytes().split(b'\0')
                    except FileNotFoundError:
                        continue
                    if str(ROOT / 'host_web/host/server.py').encode() in arguments:
                        os.kill(child, signal.SIGTERM)
                        break
                else:
                    raise AssertionError('Owned web process not found')
                assert process.wait(timeout=20) != 0, 'Unexpected child exit must fail launch'
            assert_ports_free()
            print(f'PASS {name}: HTTP / ROS graph / duplicate guard / shutdown / port cleanup')
        finally:
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
                try:
                    process.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)


async def main():
    assert_ports_free()
    await run_case(True)
    await run_case(False)
    with socket.socket() as blocker:
        blocker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        blocker.bind(('127.0.0.1', 8082))
        blocker.listen()
        result = subprocess.run(['bash', str(ROOT / 'start_host.sh'), '--check'],
                                env=ENV, capture_output=True, text=True, timeout=15)
        assert result.returncode == 1 and '8082' in result.stderr, result
    print('PASS occupied port: preflight fails without starting services')


if __name__ == '__main__':
    asyncio.run(main())
