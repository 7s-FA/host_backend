"""Five simulated ROS Action servers; refuse the real robot domain/network."""
import json
import os
from pathlib import Path
import threading
import time
import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor, ExternalShutdownException
from rclpy.node import Node
from host_pkg.action import Arm, Burger
from control import DEVICES


class MockDevices(Node):
    def __init__(self):
        super().__init__('host_mock_devices')
        self.lock = threading.RLock()
        self.active = {}
        self.delay = float(os.environ.get('HOST_MOCK_DELAY', '0.5'))
        self.fault = os.environ.get('HOST_MOCK_FAULT', '')  # e.g. arm3:LOAD_A:reject|error|stall
        self.reject_stops = False  # Test the deployed arm1 ERROR-state rejection.
        self.journal = Path(os.environ['HOST_RUNTIME_DIR']) / 'mock-events.jsonl'
        self.journal.write_text('')
        self.servers = []
        for device in DEVICES:
            action = Burger if device in ('M1', 'M2') else Arm
            self.servers.append(ActionServer(
                self, action, f'/{device}/data',
                execute_callback=lambda handle, d=device, a=action: self.execute(d, a, handle),
                goal_callback=lambda goal, d=device: self.goal(d, goal),
                cancel_callback=lambda handle: CancelResponse.REJECT,
                callback_group=ReentrantCallbackGroup()))

    def record(self, device, command, event, request_id=''):
        with self.lock, self.journal.open('a') as stream:
            stream.write(json.dumps({'device': device, 'command': command, 'event': event,
                                     'request_id': request_id, 'time': time.monotonic()}) + '\n')

    def goal(self, device, goal):
        command = goal.command
        allowed = ({'GO_TO_MAT', 'GO_TO_ASM', 'GO_TO_REST', 'GO_TO_PARK', 'RESTART'} if device in ('M1', 'M2') else
                   {'SELECT_A', 'SELECT_B', 'HOME_A', 'CLEAR_ERROR'} if device == 'arm1' else
                   {'BUILD_A', 'BUILD_B', 'BUILD_LOAD_A', 'BUILD_LOAD_B', 'BUILD_SLIDE', 'RESET', 'CLEAR_ERROR'} if device == 'arm2' else {'LOAD_A', 'LOAD_B'})
        if command == 'EMER_STOP':
            if self.reject_stops:
                self.record(device, command, 'rejected')
                return GoalResponse.REJECT
            return GoalResponse.ACCEPT
        resource = 'production' if device in ('arm2', 'arm3') else device
        with self.lock:
            if command not in allowed or resource in self.active or self.fault == f'{device}:{command}:reject':
                self.record(device, command, 'rejected')
                return GoalResponse.REJECT
            self.active[resource] = threading.Event()
        return GoalResponse.ACCEPT

    def execute(self, device, action, handle):
        command = handle.request.command
        request_id = bytes(handle.goal_id.uuid).hex()
        resource = 'production' if device in ('arm2', 'arm3') else device
        self.record(device, command, 'accepted', request_id)
        if command == 'EMER_STOP':
            with self.lock:
                stopping = self.active.get(resource)
                if stopping:
                    stopping.set()
            handle.succeed()
            self.record(device, command, 'stopped', request_id)
            return action.Result(success=True, message='IDLE')
        with self.lock:
            stopping = self.active[resource]
        handle.publish_feedback(action.Feedback(message='RUNNING'))
        duration = 60 if self.fault == f'{device}:{command}:stall' else self.delay
        interrupted = stopping.wait(duration)
        if command.startswith('BUILD_LOAD_') and not interrupted:
            handle.publish_feedback(action.Feedback(message='BUILD_DONE'))
            self.record(device, command, 'build_done', request_id)
            interrupted = stopping.wait(duration)
        failure = interrupted or self.fault == f'{device}:{command}:error'
        # Release before Result so the next serialized workcell task can be accepted.
        with self.lock:
            self.active.pop(resource, None)
        if failure:
            handle.publish_feedback(action.Feedback(message='ERROR'))
            handle.abort()
            self.record(device, command, 'failed', request_id)
            return action.Result(success=False, message='ERROR')
        handle.succeed()
        self.record(device, command, 'succeeded', request_id)
        return action.Result(success=True, message='IDLE')

    def stop_all(self):
        with self.lock:
            for event in self.active.values():
                event.set()


def main():
    if os.environ.get('ROS_DOMAIN_ID') != '149' or os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') != 'LOCALHOST':
        raise SystemExit('모의 서버는 Domain 149 / LOCALHOST에서만 실행할 수 있습니다.')
    rclpy.init()
    node = MockDevices()
    executor = MultiThreadedExecutor(num_threads=8)
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.stop_all()
        executor.shutdown(timeout_sec=2)
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
