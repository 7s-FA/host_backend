import rclpy
import time
from rclpy.node import Node
from shared_data import shared_memory

PRODUCT_OF_MATERIAL_A = 'A제품 · 부품 3개 / 세트' # 변경 가능 문구
PRODUCT_OF_MATERIAL_B = 'B제품 · 부품 3개 / 세트' # 변경 가능 문구

class RobotController(Node):
    def __init__(self, burger1_node, burger2_node, waffle_node, arm1_node, arm2_node, arm3_node):
        super().__init__('control')
        self.old_start_flag = False
        self.quantity = 0
        self.product = ""

        # Robot
        self.burger1 = burger1_node
        self.burger2 = burger2_node
        self.waffle = waffle_node

        self.burger1_state = False
        self.burger2_state = False
        # self.waffle_state = False

        self.burger1_step = "PARK"
        self.burger2_step = "PARK"
        # self.waffle_step = "내용을 작성해주세요"

        self.burger1_action = "STOP"
        self.burger2_action = "STOP"
        # self.waffle_action = "STOP"
        

        # Arm
        self.arm1 = arm1_node
        self.arm2 = arm2_node
        self.arm3 = arm3_node
        
        self.arm1_action = "STOP"
        self.arm2_action = "STOP"
        self.arm3_action = "STOP"

        self.arm1_sending_end_flag = False
        self.arm2_sending_to_bot_end_flag = False
        self.arm2_sending_to_arm_end_flag = False
        self.arm3_sending_end_flag = False # waffle에서 써야함

        self.timer = self.create_timer(1.0, self.startRobot) # print 문 빼고 나중에 0.1초로 바꾸자
        self.get_logger().info('RobotController 노드가 시작되었습니다.')

    def startRobot(self):
        if  shared_memory.start_flag == True or self.old_start_flag == True:
            if  self.old_start_flag == True:
                self.get_logger().info("Control Flow가 실행 중입니다.")

            else:
                self.get_logger().info("\033[1;32mControl Flow가 실행 됩니다.\033[0m")
                self.quantity = shared_memory.quantity
                self.product = shared_memory.product
                self.old_start_flag = True

            self.controlRobot()

            if  self.burger1_state == False and self.burger2_state == False:
                self.old_start_flag = False

        else:
            self.get_logger().info("web에서 동작 버튼을 눌러주세요.")

    def controlRobot(self):
        self.controlburger1()
        self.controlburger2()
        self.controlwaffle()

        self.controlarm1()
        self.controlarm2()
        self.controlarm3()


    def controlburger1(self):
        if  self.quantity > 0:
            self.quantity -= 1
            self.burger1_state = True

        if  self.burger1_state == True:
            if  self.burger1_step == "PARK" and (self.burger1_action == "STOP" or self.burger1_action == "RESTART") and self.burger2_action == "STOP":
                self.burger1_step = "MAT"
                self.burger1_action = "OP"

                self.burger1.send_goal("GO_TO_MAT", 100.0)

            elif self.burger1_step == "MAT" and (self.burger1_action == "STOP" or self.burger1_action == "RESTART") and self.burger2_action == "STOP" and self.arm1_sending_end_flag == True:
                
                self.burger1_step = "ASM"
                self.burger1_action = "OP"
                
                self.burger1.send_goal("GO_TO_ASM", 100.0)

            elif self.burger1_step == "ASM" and (self.burger1_action == "STOP" or self.burger1_action == "RESTART") and self.burger2_action == "STOP" and self.arm2_sending_to_bot_end_flag == True: 
                
                    self.burger1_step = "PARK"
                    self.burger1_action = "OP"
                    
                    self.burger1.send_goal("GO_TO_PARK", 100.0)

            else:
                if  shared_memory.burger1_end_flag == True:
                    shared_memory.burger1_end_flag = False
                    self.burger1_action = "STOP"

                    if  self.burger1_step == "MAT":
                        if  shared_memory.burger1_success == True and shared_memory.burger1_end_message == "IDLE":
                            self.get_logger().info("Burger1이 Mat에 도착했습니다.")

                        else:
                            self.get_logger().info("Burger1이 Mat에 도착하지 못했습니다. 재동작 합니다.")
                            self.burger1_step = "PARK"
                            self.burger1_action = "RESTART"

                    elif self.burger1_step == "ASM":
                        if  shared_memory.burger1_success == True and shared_memory.burger1_end_message == "IDLE":
                            self.get_logger().info("Burger1이 ASM에 도착했습니다.")
                            self.arm1_sending_end_flag = False

                        else:
                            self.get_logger().info("Burger1이 ASM에 도착하지 못했습니다. 재동작 합니다.")
                            self.burger1_step = "MAT"
                            self.burger1_action = "RESTART"

                    elif self.burger1_step == "PARK":
                        if  shared_memory.burger1_success == True and shared_memory.burger1_end_message == "IDLE":
                            self.get_logger().info("Burger1이 Park에 도착했습니다.")
                            self.arm2_sending_to_bot_end_flag = False
                            self.burger1_state = False
                        else:
                            self.get_logger().info("Burger1이 PARK에 도착하지 못했습니다. 재동작 합니다.")
                            self.burger1_step = "ASM"
                            self.burger1_action = "RESTART"

                    else:
                        self.get_logger().info(f"self.burger1_step 오 입력 : {self.burger1_step}")
                else:
                    self.get_logger().info("Burger1이 동작 중 입니다.")

        else:
            self.get_logger().info("burger1 동작이 종료되었습니다. 다른 장치의 동작을 기다리고 있습니다.")


    def controlburger2(self):
        if  self.quantity > 0:
            self.quantity -= 1
            self.burger2_state = True

        if  self.burger2_state == True:
                if  self.burger2_step == "PARK" and (self.burger2_action == "STOP" or self.burger2_action == "RESTART") and self.burger1_step == "MAT" and self.burger1_action == "STOP":
                    self.burger2_step = "REST"
                    self.burger2_action = "OP"
                    
                    self.burger2.send_goal("GO_TO_REST", 100.0)

                elif self.burger2_step == "REST" and (self.burger2_action == "STOP" or self.burger2_action == "RESTART") and self.burger1_step == "ASM" and self.burger1_action == "STOP":
                    self.burger2_step = "MAT"
                    self.burger2_action = "OP"
                    
                    self.burger2.send_goal("GO_TO_MAT", 100.0)

                elif self.burger2_step == "MAT" and (self.burger2_action == "STOP" or self.burger2_action == "RESTART") and self.burger1_step == "PARK" and self.burger1_action == "STOP" and self.arm1_sending_end_flag == True:
                    self.burger2_step = "ASM"
                    self.burger2_action = "OP"

                    self.burger2.send_goal("GO_TO_ASM", 100.0)

                elif self.burger2_step == "ASM" and (self.burger2_action == "STOP" or self.burger2_action == "RESTART") and self.burger1_step == "PARK" and self.burger1_action == "STOP" and self.arm2_sending_to_bot_end_flag == True:
                    self.burger2_step = "PARK"
                    self.burger2_action = "OP"

                    self.burger2.send_goal("GO_TO_PARK", 100.0)

                else:
                    if  shared_memory.burger2_end_flag == True:
                        shared_memory.burger2_end_flag = False
                        self.burger2_action = "STOP"
    
                        if  self.burger2_step == "REST":
                            if  shared_memory.burger2_success == True and shared_memory.burger2_end_message == "IDLE":
                                self.get_logger().info("Burger2이 REST에 도착했습니다.")

                            else:
                                self.get_logger().info("Burger2이 REST에 도착하지 못했습니다. 재동작 합니다.")
                                self.burger2_step = "PARK"
                                self.burger2_action = "RESTART"

                        elif self.burger2_step == "MAT":
                            if  shared_memory.burger2_success == True and shared_memory.burger2_end_message == "IDLE":
                                self.get_logger().info("Burger2이 MAT에 도착했습니다.")

                            else:
                                self.get_logger().info("Burger2이 MAT에 도착하지 못했습니다. 재동작 합니다.")
                                self.burger2_step = "REST"
                                self.burger2_action = "RESTART"

                        elif self.burger2_step == "ASM":
                            if  shared_memory.burger2_success == True and shared_memory.burger2_end_message == "IDLE":
                                self.arm1_sending_end_flag = False
                                self.get_logger().info("Burger2이 ASM에 도착했습니다.")

                            else:
                                self.get_logger().info("Burger2이 ASM에 도착하지 못했습니다. 재동작 합니다.")
                                self.burger2_step = "MAT"
                                self.burger2_action = "RESTART"

                        elif self.burger2_step == "PARK":
                            if  shared_memory.burger2_success == True and shared_memory.burger2_end_message == "IDLE":
                                self.arm2_sending_to_bot_end_flag = False
                                self.burger2_state = False
                                self.get_logger().info("Burger2이 PARK에 도착했습니다.")

                            else:
                                self.get_logger().info("Burger2이 PARK에 도착하지 못했습니다. 재동작 합니다.")
                                self.burger2_step = "ASM"
                                self.burger2_action = "RESTART"
                        else:
                            self.get_logger().info(f"self.burger2_step 오 입력 : {self.burger2_step}")
                    else:
                        self.get_logger().info("Burger2이 동작 중 입니다.")
        else:
            self.get_logger().info("burger2 동작이 종료되었습니다. 다른 장치의 동작을 기다리고 있습니다.")

    def controlwaffle(self):
        self.get_logger().info("waffle 은 미구현 입니다. 개빡치게 하지마세요.")

    def controlarm1(self):
        if  self.arm1_action == "STOP" and ((self.burger1_step == "MAT" and self.burger1_action == "STOP") or (self.burger2_step == "MAT" and self.burger2_action == "STOP")):
            self.arm1_action = "OP"

            if self.product == PRODUCT_OF_MATERIAL_A:
                self.arm1.send_goal("SELECT_A")
            else:
                self.arm1.send_goal("SELECT_B")

        else:
            if  shared_memory.arm1_end_flag == True:
                shared_memory.arm1_end_flag = False
                self.arm1_action = "STOP"

                if  shared_memory.amr1_success == True and shared_memory.amr1_end_message == "IDLE":
                    self.get_logger().info("Arm1 동작에 성공했습니다.")
                    self.arm1_sending_end_flag = True

                else:
                    self.arm1_action = "STOP"
                    self.get_logger().info("Arm1 동작에 실패했습니다. 재동작 합니다.")
            else:
                self.get_logger().info("Arm1이 동작 중 입니다.")


    def controlarm2(self):
        if  self.arm2_action == "STOP" and ((self.burger1_step == "ASM" and self.burger1_action == "STOP") or (self.burger2_step == "ASM" and self.burger2_action == "STOP")):
            self.arm2_action = "OP"

            if self.product == PRODUCT_OF_MATERIAL_A:
                self.arm2.send_goal("BUILD_A")
            else:
                self.arm2.send_goal("BUILD_B")

        else:
            if  shared_memory.arm2_end_flag == True:
                shared_memory.arm2_end_flag = False
                self.arm2_action = "STOP"

                if  shared_memory.amr2_success == True and shared_memory.amr2_end_message == "IDLE":
                    self.get_logger().info("Arm2 동작에 성공했습니다.")
                    self.arm2_sending_to_bot_end_flag = True
                    self.arm2_sending_to_arm_end_flag = True

                else:
                    self.arm2_action = "STOP"
                    self.get_logger().info("Arm2 동작에 실패했습니다. 재동작 합니다.")
            else:
                self.get_logger().info("Arm2이 동작 중 입니다.")

    
    def controlarm3(self):
        if  self.arm3_action == "STOP" and self.arm2_sending_to_arm_end_flag == True:
            self.arm3_action = "OP"

            if self.product == PRODUCT_OF_MATERIAL_A:
                self.arm3.send_goal("LOAD_A")
            else:
                self.arm3.send_goal("LOAD_B")

        else:
            if  shared_memory.arm3_end_flag == True:
                shared_memory.arm3_end_flag = False
                self.arm3_action = "STOP"

                if  shared_memory.amr3_success == True and shared_memory.amr3_end_message == "IDLE":
                    self.get_logger().info("Arm3 동작에 성공했습니다.")
                    self.arm3_sending_end_flag = True # waffle에서 써야함
                    self.arm2_sending_to_arm_end_flag = False

                else:
                    self.arm3_action = "STOP"
                    self.get_logger().info("Arm3 동작에 실패했습니다. 재동작 합니다.")
            else:
                self.get_logger().info("Arm3이 동작 중 입니다.")