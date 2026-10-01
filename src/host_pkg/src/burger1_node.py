import rclpy

from rclpy.action import ActionClient
from rclpy.node import Node
from host_pkg.action import Burger

from shared_data import shared_memory

class Burger1ActionClient(Node):
    def __init__(self):
        # 네임스페이스 'host' 지정 및 노드 이름 설정
        super().__init__('data', namespace='M1') # 발행을 /M1/host_data 로 할꺼임
        self._client = ActionClient(self, Burger, '/M1/data') # 수신을 /host_server/robot_data 로 할꺼임

    def send_goal(self, command, speed):

        self.get_logger().info('Waiting for action server at /host/M1...')
        self._client.wait_for_server()

        goal_msg = Burger.Goal()
        goal_msg.command = command
        goal_msg.cmd_val = speed

        self.get_logger().info(f"Goal msg CMD = {command}, Speed = {speed}")

        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_data):
        shared_memory.burger1_x_axis = feedback_data.feedback.robot_x
        shared_memory.burger1_y_axis = feedback_data.feedback.robot_y
        shared_memory.burger1_theta = feedback_data.feedback.robot_theta # string Data
        shared_memory.key = False

        self.get_logger().info(f"\033[1;31mx_axis = {shared_memory.burger1_x_axis}, y_axis = {shared_memory.burger1_y_axis}, theta = {shared_memory.burger1_theta}\033[0m")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("\033[1;31mburger1 fail\033[0m")
            # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
            return

        self.get_logger().info("\033[1;31mburger1 success\033[0m")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        
    def get_result_callback(self, future):
        result = future.result().result

        shared_memory.burger1_end_flag = True
        shared_memory.burger1_success = result.success
        shared_memory.burger1_end_message = result.message

        self.get_logger().info(f'Result received: success={result.success}, message="{result.message}"')
        # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
