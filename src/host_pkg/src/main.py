"""Host runtime: web order adapter + result-driven controller + ROS Action clients."""
import json
import math
import os
from pathlib import Path
import queue
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String
from action_transport import ActionTransport
from continuous_process import ContinuousProcessController as ProcessController
from http_adapter import HttpAdapter


def positive_setting(name, default, maximum):
    value = float(os.environ.get(name, default))
    if not math.isfinite(value) or not 0 < value <= maximum:
        raise ValueError(f'{name}: 0 초과 {maximum} 이하의 유한 값이 필요합니다.')
    return value


class HostRuntime(Node):
    def __init__(self):
        super().__init__('control')
        self.events = queue.Queue()
        self.transport = ActionTransport(self, self.events, positive_setting('HOST_SPEED_PERCENT', 100, 100))
        self.bridge = HttpAdapter(os.environ.get('ROBOT3_BRIDGE_TOKEN', ''))
        mode = 'mock' if os.environ.get('HOST_MOCK') == '1' else 'hardware'
        runtime = Path(os.environ.get('HOST_RUNTIME_DIR', Path(__file__).resolve().parents[4] / '.runtime/host'))
        state_file = os.environ.get('HOST_STATE_FILE', str(runtime / ('order-' + mode + '.json')))
        self.controller = ProcessController(
            self.transport, state_file=state_file, mode=mode,
            manual_inspection=os.environ.get('HOST_MANUAL_INSPECTION') == '1',
            goal_timeout=positive_setting('HOST_GOAL_TIMEOUT', 5, 60),
            motion_timeout=positive_setting('HOST_MOTION_TIMEOUT', 300, 3600),
            arm_timeout=positive_setting('HOST_ARM_TIMEOUT', 600, 3600))
        self.publisher = self.create_publisher(String, '/ros_to_web', 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.bridge.set_report(self.controller.snapshot())
        self.bridge.start()
        self.get_logger().info(f'관제 준비 · {mode} · 새 주문 병렬 계획 parallel-v1 · 기존 주문 유지 · 주문 수신 전 동작 없음')

    def tick(self):
        for _ in range(100):
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            self.controller.event(*event)
        # Set connectivity before processing a newly received user command.
        connected = self.bridge.connected()
        self.controller.link = connected
        self.controller.ready = self.transport.ready()
        for _ in range(100):
            try:
                command = self.bridge.commands.get_nowait()
            except queue.Empty:
                break
            if command.get('action') == '_session_changed':
                self.controller.fail('웹 API 서버가 재시작되었습니다.', uncertain=True)
            else:
                self.controller.command(command)
        self.controller.tick(connected)
        report = self.controller.snapshot()
        self.bridge.set_report(report)
        self.publisher.publish(String(data=json.dumps({'protocol': 2, 'host_mode': report['runtime_mode'],
                                                       'order': report['order'], 'message': 'Host 상태'}, ensure_ascii=False)))

    def close(self):
        if self.controller.reset_busy():
            self.controller.abort_full_reset('관제 종료 · 전체 초기화 결과 확인 필요')
        elif (self.controller.active or {}).get('preparation'):
            self.controller.note('관제 종료 · 주차 준비 결과 확인 필요')
            self.controller.save()
        elif (self.controller.active or {}).get('manual'):
            self.controller.fail_manual('관제 프로세스 종료 · 수동 이동 결과 미확인')
        else:
            self.controller.fail('관제 프로세스 종료 · 작업 결과 미확인', uncertain=True)
        self.bridge.close()
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = HostRuntime()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node:
            node.close()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
