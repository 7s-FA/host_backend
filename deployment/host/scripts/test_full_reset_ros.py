#!/usr/bin/env python3
"""Real Action transport with localhost-only fake devices; never contact hardware."""
import json
import os
from pathlib import Path
import queue
import sys
import tempfile
import time
import uuid

if os.environ.get('ROS_DOMAIN_ID') != '149' or os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') != 'LOCALHOST':
    raise SystemExit('Refusing test outside Domain 149 / LOCALHOST')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'host_backend/src/host_pkg/src'))
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from action_transport import ActionTransport
from mock_devices import MockDevices
from full_reset import FullResetController
from initial_state import INITIAL_STEPS


def main():
    with tempfile.TemporaryDirectory(prefix='full-reset-ros-') as folder:
        os.environ.update(HOST_RUNTIME_DIR=folder, HOST_MOCK_DELAY='.1', HOST_MOCK_FAULT='')
        rclpy.init()
        mock, host = MockDevices(), Node('initialization_mock_host')
        events = queue.Queue()
        transport = ActionTransport(host, events)
        executor = MultiThreadedExecutor(num_threads=8)
        executor.add_node(mock); executor.add_node(host)
        try:
            for fault in ('', 'arm2:BUILD_SLIDE:error', 'M1:GO_TO_PARK:reject', 'arm1:HOME_A:error'):
                mock.fault = fault
                mock.reject_stops = fault == 'arm1:HOME_A:error'
                core = FullResetController(transport, mode='mock', goal_timeout=4)
                def until(predicate):
                    deadline = time.monotonic()+30
                    while time.monotonic()<deadline:
                        executor.spin_once(timeout_sec=.01)
                        while not events.empty(): core.event(*events.get_nowait())
                        core.tick(True)
                        if predicate(): return
                    raise AssertionError(core.snapshot())
                until(core.can_full_reset)
                start = len(mock.journal.read_text().splitlines())
                core.command(dict(id=uuid.uuid4().hex, action='full_reset', operator_confirmed=True,
                                  order_id=None, recovery_revision=0))
                until(lambda: core.full_reset['status'] in ('done','failed') and not core.reset_busy())
                logs = [json.loads(line) for line in mock.journal.read_text().splitlines()[start:]]
                accepted = [(row['device'],row['command']) for row in logs if row['event']=='accepted']
                if not fault:
                    assert core.full_reset['status']=='done', core.snapshot()
                    assert accepted==[step[:2] for step in INITIAL_STEPS], accepted
                    assert core.snapshot()['can_start']
                else:
                    assert core.full_reset['status']=='failed'
                    assert ('M2','GO_TO_PARK') not in accepted
                    if fault.startswith('arm2:'):
                        assert ('M1','GO_TO_PARK') not in accepted
                    if mock.reject_stops:
                        assert any(r['command']=='EMER_STOP' and r['event']=='rejected' for r in logs), logs
                        assert core.can_full_reset(), core.snapshot()
                        assert not core.snapshot()['can_start']
                print('PASS ROS initialization: '+(fault or 'all 9 steps, exact order, confirmed Results'), flush=True)
        finally:
            mock.stop_all(); executor.shutdown(timeout_sec=5)
            host.destroy_node(); mock.destroy_node(); rclpy.try_shutdown()


if __name__=='__main__':main()
