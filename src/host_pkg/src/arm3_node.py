import rclpy

from rclpy.action import ActionClient
from rclpy.node import Node
from host_pkg.action import Arm

from shared_data import shared_memory

class Arm3ActionClient(Node):
    def __init__(self):
        # 네임스페이스 'host' 지정 및 노드 이름 설정
        super().__init__('data', namespace='arm3') # 발행을 /Arm3/data 로 할꺼임
        self._client = ActionClient(self, Arm, '/arm3/data') # 수신을 /Arm3/data 로 할꺼임

    def send_goal(self, command):

        self.get_logger().info('Waiting for action server at /host/arm3...')
        self._client.wait_for_server()

        goal_msg = Arm.Goal()
        goal_msg.command = command

        self.get_logger().info(f"Goal msg CMD = {command}")

        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_data):
        shared_memory.arm3_feedback_msg = feedback_data.feedback.message
        
        self.get_logger().info(f"\033[1;31mFeedback_MSG = {shared_memory.arm3_feedback_msg}\033[0m")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("\033[1;31mArm3 fail\033[0m")
            # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
            return

        self.get_logger().info("\033[1;31mArm3 success\033[0m")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        
    def get_result_callback(self, future):
        result = future.result().result

        shared_memory.arm3_end_flag = True
        shared_memory.arm3_success = result.success
        shared_memory.arm3_end_message = result.message

        self.get_logger().info(f'Result received: success={shared_memory.arm3_success}, message="{shared_memory.arm3_end_message}"')
        # rclpy.shutdown() # 프로그램 자체를 꺼버리는 거
