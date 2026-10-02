import rclpy
import time
from rclpy.node import Node
from shared_data import shared_memory

class RobotController(Node):
    def __init__(self, burger1_node, burger2_node): # 이거 말고 밑에꺼 써야함
    # def __init__(self, burger1_node, burger2_node, waffle_node, arm1_node, arm2_node, arm3_node):
        super().__init__('control')
        self.old_start_flag = False
        
        # Robot
        self.burger1 = burger1_node
        self.burger2 = burger2_node
        # self.waffle = waffle_node

        # # Arm
        # self.arm1 = arm1_node
        # self.arm2 = arm2_node
        # self.arm3 = arm3_node

        self.timer = self.create_timer(1.0, self.controlRobot) # print 문 빼고 나중에 0.1초로 바꾸자
        self.get_logger().info('RobotController 노드가 시작되었습니다.')

    def controlRobot(self):
        
        if  self.old_start_flag == shared_memory.start_flag:
            # no operate
            self.get_logger().info("정상 종료 : 이전 상태와 동일한 상태 입력 / 현 동작 유지")
        else:
            self.old_start_flag = shared_memory.start_flag

            if  self.old_start_flag == True:
                self.get_logger().info("\033[1;31m로봇 동작 시작\033[0m")
                
                if shared_memory.quantity >= 2:
                    self.controlMultiRobot()
                else:
                    self.controlSingleRobot()
                
                
                
                # 동작 내용
                # self.burger1.send_goal("GO_TO_MAT", 3)
                # self.burger2.send_goal("GO_TO_MAT", 5)
            else:
                self.get_logger().info("\033[1;31m로봇 정지\033[0m")

    def controlSingleRobot(self):
        self.get_logger().info("Single Robot Flow - only Burger1 moves")
        self.burger1.send_goal("GO_TO_MAT", 99.0) # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경

        while shared_memory.burger1_end_flag == False:
            time.sleep(0.1)
            
        shared_memory.burger1_end_flag = False

        time.sleep(0.001) # 짧은 대기 시간
        if shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":
            self.get_logger().info("ENDENDENDENDENDENDENDENDENDENDEND")


    def controlMultiRobot(self):
        self.get_logger().info("Multi Robot Flow - Both Robotes move")
        self.burger1.send_goal("GO_TO_MAT", 99.0) # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경

        while shared_memory.burger1_end_flag == False:
            time.sleep(0.1)
            
        shared_memory.burger1_end_flag = False

        time.sleep(0.001) # 짧은 대기 시간
        if shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":
            self.burger2.send_goal("GO_TO_REST", 99.0) # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경

            while shared_memory.burger2_end_flag == False:
                time.sleep(0.1)

            shared_memory.burger2_end_flag = False

            time.sleep(0.001) # 짧은 대기 시간

        # Test를 위해 Burger 1 -> 재료 , Burger 2 대기 장소 까지 이동만 시킴