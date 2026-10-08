import threading
import time

from rclpy.action import ActionClient
from rclpy.node import Node
from host_pkg.action import Burger

from shared_data import shared_memory

SERVER_WAIT_SEC = 5.0 # Action 서버가 없을 때 무한 대기하지 않기 위한 제한

class BurgerActionClient(Node):
    """버거 로봇 한 대의 Action 클라이언트. 결과는 shared_memory.<prefix>_* 에 기록한다.

    로봇(AMR) 서버는 정지·취소·실패가 나면 정지 래치를 걸고 RESTART 를 받기 전까지 새 이동을 거부한다.
    그래서 이동이 정상 완료되지 않은 로봇은 needs_restart 로 표시하고, 다음 이동 전에 RESTART 를 먼저 보낸다.
    """

    def __init__(self, robot_id, prefix):
        # 네임스페이스로 로봇 구분 (/M1, /M2)
        super().__init__('data', namespace=robot_id)
        self._robot_id = robot_id
        self._prefix = prefix
        self._client = ActionClient(self, Burger, f'/{robot_id}/data')
        self._goal_handle = None
        self._generation = 0 # 취소/재전송 된 이전 goal 의 늦은 응답을 구분하기 위한 번호
        self.moving = False # 이동 goal 이 진행 중인지
        self.needs_restart = False # 정상 완료되지 않아 로봇에 정지 래치가 걸렸을 수 있는지

    def _set(self, field, value):
        setattr(shared_memory, f'{self._prefix}_{field}', value)

    def _finish(self, success, message):
        # 결과 값을 먼저 쓰고 end_flag 를 마지막에 올려야 control 이 이전 값을 읽지 않음
        self.moving = False
        if not success:
            self.needs_restart = True
        self._set('success', success)
        self._set('end_message', message)
        self._set('end_flag', True)

    def send_goal(self, command, speed):
        self._generation += 1
        generation = self._generation
        self._goal_handle = None

        # 이전 동작의 결과가 남아 있으면 새 동작이 바로 끝난 것으로 오인하므로 먼저 초기화
        self._set('end_flag', False)
        self._set('success', False)
        self._set('end_message', "")

        self.get_logger().info(f'Waiting for action server at /{self._robot_id}/data...')
        if not self._client.wait_for_server(timeout_sec=SERVER_WAIT_SEC):
            self.get_logger().error(f"\033[1;31m{self._prefix} Action 서버 응답 없음 ({SERVER_WAIT_SEC}s)\033[0m")
            self._finish(False, "SERVER_UNAVAILABLE")
            return False

        goal_msg = Burger.Goal()
        goal_msg.command = command
        goal_msg.cmd_val = speed

        self.get_logger().info(f"Goal msg CMD = {command}, Speed = {speed}")

        self.moving = True
        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(
            lambda future: self.goal_response_callback(future, generation))
        return True

    def send_control(self, command, timeout=10.0):
        """EMER_STOP / RESTART 같은 제어 명령을 보내고 성공 여부를 반환한다 (호출 스레드에서 블로킹).

        이동 goal 과 동시에 보낼 수 있도록 이동용 상태(generation, end_flag)는 건드리지 않는다.
        """
        if not self._client.wait_for_server(timeout_sec=SERVER_WAIT_SEC):
            self.get_logger().error(f"{self._prefix} {command} 실패 : Action 서버 응답 없음")
            return False

        goal_msg = Burger.Goal()
        goal_msg.command = command
        goal_msg.cmd_val = 0.0

        deadline = time.monotonic() + timeout
        future = self._client.send_goal_async(goal_msg)
        while not future.done():
            if time.monotonic() > deadline:
                self.get_logger().error(f"{self._prefix} {command} 접수 응답 시간 초과")
                return False
            time.sleep(0.02)
        handle = future.result()
        if not handle.accepted:
            self.get_logger().warning(f"{self._prefix} {command} 거절됨")
            return False

        result_future = handle.get_result_async()
        while not result_future.done():
            if time.monotonic() > deadline:
                self.get_logger().error(f"{self._prefix} {command} 결과 응답 시간 초과")
                return False
            time.sleep(0.02)
        result = result_future.result().result
        self.get_logger().info(f'{self._prefix} {command} 결과: success={result.success}, message="{result.message}"')
        return bool(result.success)

    def cancel_goal(self):
        """진행 중인 goal 이 있으면 취소를 요청한다."""
        goal_handle = self._goal_handle
        if goal_handle is None:
            return
        self.get_logger().info(f"\033[1;31m{self._prefix} goal 취소 요청\033[0m")
        goal_handle.cancel_goal_async()

    def feedback_callback(self, feedback_data):
        self._set('x_axis', feedback_data.feedback.robot_x)
        self._set('y_axis', feedback_data.feedback.robot_y)
        self._set('theta', feedback_data.feedback.robot_theta) # string Data
        shared_memory.key = False

        self.get_logger().info(
            f"\033[1;31mx_axis = {getattr(shared_memory, self._prefix + '_x_axis')}, "
            f"y_axis = {getattr(shared_memory, self._prefix + '_y_axis')}, "
            f"theta = {getattr(shared_memory, self._prefix + '_theta')}\033[0m",
            throttle_duration_sec=1.0)

    def goal_response_callback(self, future, generation):
        if generation != self._generation:
            return # 이미 새 goal 로 교체됨
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info(f"\033[1;31m{self._prefix} fail\033[0m")
            self._finish(False, "GOAL_REJECTED")
            return

        self.get_logger().info(f"\033[1;31m{self._prefix} success\033[0m")
        self._goal_handle = goal_handle
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(
            lambda future: self.get_result_callback(future, generation))

    def get_result_callback(self, future, generation):
        if generation != self._generation:
            return # 취소되었거나 교체된 goal 의 늦은 결과는 무시
        self._goal_handle = None
        result = future.result().result

        self._finish(result.success, result.message)

        self.get_logger().info(f'Result received: success={result.success}, message="{result.message}"')
