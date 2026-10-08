import rclpy
import json
import time

from rclpy.node import Node
from std_msgs.msg import String

from shared_data import shared_memory
from control import RobotController

class WebDataPase(Node):
    def __init__(self):
        super().__init__('web_data_receiver')
        self.subscription = self.create_subscription(
            String,
            '/web_to_ros',
            self.listener_callback,
            10
        )

        # 2. ROS에서 웹으로 데이터를 보내는 발행자 (Publisher)
        self.publisher = self.create_publisher(
            String,
            '/ros_to_web',
            10
        )

        self._last_received = None
        self._last_status = None
        self._last_sent_at = 0.0

        # 3. 주기적으로(예: 0.2초마다) 웹으로 로봇/공정 상태를 전송하는 타이머 설정
        self.timer = self.create_timer(0.2, self.send_status_to_web)

        self.get_logger().info('웹 데이터 노드가 시작되었습니다.')

    def listener_callback(self, msg):
        try:
            # 웹에서 JSON 문자열로 보낸 데이터를 딕셔너리로 변환
            data = json.loads(msg.data)

            if not isinstance(data, dict):
                self.get_logger().warning(f"JSON 객체가 아닌 데이터 수신 : {msg.data}")
                return

            # 값이 하나라도 잘못되면 공유 상태를 일부만 바꾸지 않도록 먼저 모두 변환한 뒤 반영
            product = data.get('product')
            quantity = float(data.get('quantity'))
            start_flag = bool(data.get('playing'))

            shared_memory.product = product
            shared_memory.quantity = quantity
            shared_memory.start_flag = start_flag

            # 웹은 같은 값을 계속 보내므로 값이 바뀔 때만 출력
            received = (start_flag, quantity, product)
            if received != self._last_received:
                self._last_received = received
                self.get_logger().info(f"[수신 성공] 시작 여부 : {shared_memory.start_flag} 수량 : {shared_memory.quantity} 제품 : {shared_memory.product}")

            shared_memory.key = False

        except json.JSONDecodeError:
            # JSON 형태가 아닐 경우 일반 문자열로 처리
            self.get_logger().info(f"Jason 이 아닌 데이터 수신 : {msg.data}")
        except (TypeError, ValueError):
            # quantity 가 없거나 숫자가 아닌 경우 : 이전 상태를 유지하고 노드가 죽지 않게 한다
            self.get_logger().warning(f"잘못된 웹 데이터 수신, 무시함 : {msg.data}")

    def send_status_to_web(self):
        """ROS 2에서 처리된 최신 상태를 웹으로 송신하는 함수"""
        status_data = {
            "burger1_x_axis" : shared_memory.burger1_x_axis,
            "burger1_y_axis" : shared_memory.burger1_y_axis,
            "burger1_theta" : shared_memory.burger1_theta,

            "burger2_x_axis" : shared_memory.burger2_x_axis,
            "burger2_y_axis" : shared_memory.burger2_y_axis,
            "burger2_theta" : shared_memory.burger2_theta,

            "message": "ROS 2 test 공정 입니다."
        }
        
        # 받는 쪽이 없으면 직렬화·발행을 생략하고, 있어도 값이 바뀌었거나 1초가 지났을 때만 보낸다.
        if self.publisher.get_subscription_count() == 0:
            return
        now = time.monotonic()
        if status_data == self._last_status and now - self._last_sent_at < 1.0:
            return
        self._last_status = status_data
        self._last_sent_at = now

        msg = String()
        msg.data = json.dumps(status_data)
        self.publisher.publish(msg)
        # self.get_logger().info('웹으로 상태 데이터 전송 완료')