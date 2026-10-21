#!/usr/bin/env python3
"""Real ROS transport -> five mock Action servers, isolated localhost Domain 149.
No HTTP request to the live server; no robot network discovery or motion.
"""
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
sys.path.insert(0, str(ROOT/'host_web/host'))
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from action_transport import ActionTransport
from mock_devices import MockDevices
from parallel_process import ParallelProcessController
from live_control import LiveControl


def main():
    with tempfile.TemporaryDirectory(prefix='parallel-ros-') as folder:
        os.environ.update(HOST_RUNTIME_DIR=folder, HOST_MOCK_DELAY='.15', HOST_MOCK_FAULT='')
        rclpy.init()
        mock = MockDevices()
        host = Node('parallel_mock_host')
        events = queue.Queue()
        transport = ActionTransport(host, events)
        core = ParallelProcessController(transport, mode='mock', goal_timeout=3, arm_timeout=2)
        live = LiveControl('test-only')
        revision = 0
        controller_id = uuid.uuid4().hex
        executor = MultiThreadedExecutor(num_threads=8)
        executor.add_node(mock); executor.add_node(host)

        def poll():
            nonlocal revision
            executor.spin_once(timeout_sec=.01)
            while not events.empty(): core.event(*events.get_nowait())
            core.tick(True)
            revision += 1
            live.update(dict(core.snapshot(), revision=revision, controller_id=controller_id), 'test-only')
            for command in live.pending('test-only'): core.command(command)
            assert sum(t['device'] in ('M1','M2') for t in core.inflight.values()) <= 1
            assert sum(t['device'] in ('arm2','arm3') for t in core.inflight.values()) <= 1

        def until(predicate, timeout=20):
            deadline = time.monotonic()+timeout
            while time.monotonic()<deadline:
                poll()
                if predicate(): return
            raise AssertionError(core.snapshot())

        try:
            until(lambda:core.snapshot()['can_start'])
            all_overlaps = set()
            for quantity in (1,2):
                for product in ('A','B'):
                    live.issue('start',dict(product_type=product,quantity=quantity))
                    until(lambda:core.order and core.order['status']=='running')
                    deadline = time.monotonic()+20
                    while core.order['status']=='running' and time.monotonic()<deadline:
                        all_overlaps.add(tuple(sorted(t['index'] for t in core.inflight.values())))
                        poll()
                    assert core.order['status']=='done', core.snapshot()
                    assert core.order['completed']==quantity
                    assert core.order['transport_remaining']==core.order['product_remaining']==0
                    print(f'PASS ROS + API report/queue {product} x {quantity}: {len(core.finished)} results', flush=True)
            assert any({0,14}<=set(x) or {0,6}<=set(x) for x in all_overlaps), all_overlaps
            assert any({1,2}<=set(x) for x in all_overlaps), all_overlaps
            assert any({4,5}<=set(x) for x in all_overlaps), all_overlaps
            assert any({10,11}<=set(x) for x in all_overlaps), all_overlaps
            assert any({3,5}<=set(x) for x in all_overlaps), all_overlaps
            assert any({4,8}<=set(x) for x in all_overlaps), all_overlaps
            mock.fault = 'arm1:SELECT_A:error'
            live.issue('start',dict(product_type='B',quantity=2)) # no fault for B; test pause
            until(lambda:core.order['status']=='running' and len(core.inflight)==2)
            live.issue('pause',{})
            until(lambda:core.order['status']=='paused')
            count=len(core.finished)
            for _ in range(10):poll()
            assert len(core.finished)==count and not core.inflight
            live.issue('resume',{});until(lambda:core.order['status']=='done')
            print('PASS ROS pause/resume drains parallel tasks before next wave',flush=True)
            live.issue('start',dict(product_type='A',quantity=2))
            until(lambda:core.order['status']=='failed')
            until(lambda:core.can_recover())
            finished = core.finished.copy()
            assert 2 not in finished
            mock.fault=''
            report=live.state()['order']
            live.issue('retry',dict(order_id=report['id'],stage=report['stage'],
                                   recovery_revision=report['recovery_revision'],operator_confirmed=True))
            until(lambda:core.order['status']=='done')
            assert core.order['completed']==2
            print('PASS ROS fault/retry preserves completed parallel work',flush=True)
            print('PASS isolated Domain 149 / LOCALHOST; real robots and live HTTP untouched',flush=True)
        finally:
            mock.stop_all()
            executor.shutdown(timeout_sec=3)
            host.destroy_node();mock.destroy_node();rclpy.shutdown()

if __name__=='__main__':main()
