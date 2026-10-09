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

        # Arm
        self.arm1 = arm1_node
        self.arm2 = arm2_node
        self.arm3 = arm3_node

        self.timer = self.create_timer(1.0, self.controlRobot) # print 문 빼고 나중에 0.1초로 바꾸자
        self.get_logger().info('RobotController 노드가 시작되었습니다.')

    def controlRobot(self):
        
        
        if shared_memory.start_flag == True and self.old_start_flag == True:
            self.old_start_flag = shared_memory.start_flag
            self.get_logger().info("shared_memory start Flag == True && old_start_flag == True... \033[1;31m오동작 상태입니다. 확인하세요.\033[0m")
            

        elif shared_memory.start_flag == True and self.old_start_flag == False:
            self.old_start_flag = shared_memory.start_flag
            self.get_logger().info("\033[1;32m동작 Flow 진입\033[0m")

            determined_robot_count = self.select_robot_activation_strategy()

            if determined_robot_count == "MULTI_ROBOT_OPERATION":
                self.controlMultiRobot()
            elif determined_robot_count == "SINGLE_ROBOT_OPERATION":
                self.controlSingleRobot()
            else:
                self.get_logger().info(f"\033[1;32mError : determined_robot_count 값 : {determined_robot_count}\033[0m")
                
            shared_memory.start_flag = False # 해당 elif문의 마무리는 이 줄이어야 함

        elif shared_memory.start_flag == False and self.old_start_flag == True:
            self.old_start_flag = shared_memory.start_flag    
            self.get_logger().info("\033[1;31m동작이 종료되었습니다.\033[0m")

        else:
            self.old_start_flag = shared_memory.start_flag
            self.get_logger().info("미 동작 중 입니다.")
        

    def select_robot_activation_strategy(self):
        if  shared_memory.product == PRODUCT_OF_MATERIAL_A:
            self.product = PRODUCT_OF_MATERIAL_A
            if  shared_memory.remaining_material_A > shared_memory.quantity:
                shared_memory.remaining_material_A = shared_memory.remaining_material_A - shared_memory.quantity
                self.shoartage_parts = 0
            else:
                self.shoartage_parts = shared_memory.quantity - shared_memory.remaining_material_A
                shared_memory.remaining_material_A = 0
                self.get_logger().info(f"\033[1;31mA 제품이 {self.shoartage_parts}개가 부족합니다.\033[0m")
        else:
            self.product = PRODUCT_OF_MATERIAL_B
            if  shared_memory.remaining_material_B > shared_memory.quantity:
                shared_memory.remaining_material_B = shared_memory.remaining_material_B - shared_memory.quantity
                self.shoartage_parts = 0
            else:
                self.shoartage_parts = shared_memory.quantity - shared_memory.remaining_material_B
                shared_memory.remaining_material_B = 0
                self.get_logger().info(f"\033[1;31mB 제품이 {self.shoartage_parts}개가 부족합니다.\033[0m")

        self.quantity = shared_memory.quantity - self.shoartage_parts

        if self.quantity >= 2:
            return "MULTI_ROBOT_OPERATION"
        else:
            return "SINGLE_ROBOT_OPERATION"

    def controlSingleRobot(self):
        self.get_logger().info("Single Robot Flow - only Burger1 moves")
        self.burger1.send_goal("GO_TO_MAT", 100.0) # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경

        while shared_memory.burger1_end_flag == False:
            time.sleep(0.01) 

        shared_memory.burger1_end_flag = False
        if  shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":
            if self.product == PRODUCT_OF_MATERIAL_A:
                self.arm1.send_goal("SELECT_A")
            else:
                self.arm1.send_goal("SELECT_B")

            while shared_memory.arm1_end_flag == False:
                time.sleep(0.01)

            shared_memory.arm1_end_flag = False
            if  shared_memory.arm1_success == True and shared_memory.arm1_end_message == "IDLE":
                self.burger1.send_goal("GO_TO_ASM", 100.0)

                while shared_memory.burger1_end_flag == False:
                    time.sleep(0.01) 

                shared_memory.burger1_end_flag = False
                if  shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":

                    if self.product == PRODUCT_OF_MATERIAL_A:
                        self.arm2.send_goal("build_a")
                    else:
                        self.arm2.send_goal("build_b")

                    while shared_memory.arm2_end_flag == False:
                        time.sleep(0.01) 
        
                    shared_memory.arm2_end_flag = False
                    if  shared_memory.arm2_success == True and shared_memory.arm2_end_message == "IDLE":
                        # self.get_logger().info("\033[1;32mSingle 동작 정상 완료\033[0m")
                        if self.product == PRODUCT_OF_MATERIAL_A:
                            self.arm3.send_goal("load_a")
                        else:
                            self.arm3.send_goal("load_b")

                        if  shared_memory.arm3_success == True and shared_memory.arm3_end_message == "IDLE":
                            self.get_logger().info("\033[1;32mSingle 동작 정상 완료\033[0m")
                        else:
                            self.get_logger().info("\033[1;arm3 동작에 실패했습니다. 다시 시작해주세요.\033[0m")

                else:
                    self.get_logger().info("\033[1;31mburger1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")

            else:
                self.get_logger().info("\033[1;31marm1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")
            
        else:
            self.get_logger().info("\033[1;31mburger1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")
    
    
    
    def controlMultiRobot(self): # 2개일 때 동작
        self.get_logger().info("Multi Robot Flow - only Burger1 moves")
        self.burger1.send_goal("GO_TO_MAT", 100.0) # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경

        while shared_memory.burger1_end_flag == False:
            time.sleep(0.01) 

        shared_memory.burger1_end_flag = False

        if  shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":
            if self.product == PRODUCT_OF_MATERIAL_A:
                self.arm1.send_goal("SELECT_A")
            else:
                self.arm1.send_goal("SELECT_B")

            self.burger2.send_goal("GO_TO_REST", 100.0)

            while (shared_memory.arm1_end_flag == False) or (shared_memory.burger2_end_flag == False):
                time.sleep(0.01) 

            shared_memory.burger2_end_flag = False
            shared_memory.arm1_end_flag = False
            if  shared_memory.arm1_success == True and shared_memory.arm1_end_message == "IDLE":
                if  shared_memory.burger2_end_flag == True and shared_memory.burger2_end_message == "IDLE":
                    self.burger1.send_goal("GO_TO_ASM", 100.0)
    
                    while shared_memory.burger1_end_flag == False:
                        time.sleep(0.01) 
    
                    shared_memory.burger1_end_flag = False
                    if  shared_memory.burger1_success == True and shared_memory.burger1_message == "IDLE":
    
                        if self.product == PRODUCT_OF_MATERIAL_A:
                            self.arm2.send_goal("build_a")
                        else:
                            self.arm2.send_goal("build_b")

                        self.burger1.send_goal("GO_TO_MAT", 100.0)

                        while (shared_memory.arm2_end_flag == False) or (shared_memory.burger1_end_flag == False):
                            time.sleep(0.01) 



                            if  shared_memory.arm2_end_flag == True:
                                first_end_scnario = "ARM"
                                if self.product == PRODUCT_OF_MATERIAL_A:
                                    self.arm3.send_goal("load_a")
                                else:
                                    self.arm3.send_goal("load_b")
                                
                            if  shared_memory.burger1_end_flag == True:
                                first_end_scnario = "BURGER"
                                if self.product == PRODUCT_OF_MATERIAL_A:
                                    self.arm1.send_goal("SELECT_A")
                                else:
                                    self.arm1.send_goal("SELECT_B")
                                
                        shared_memory.burger1_end_flag = False
                        shared_memory.arm2_end_flag = False

                        if first_end_scnario == "ARM":
                            if self.product == PRODUCT_OF_MATERIAL_A:
                                self.arm1.send_goal("SELECT_A")
                            else:
                                self.arm1.send_goal("SELECT_B")

                        else:
                            if self.product == PRODUCT_OF_MATERIAL_A:
                                self.arm3.send_goal("load_a")
                            else:
                                self.arm3.send_goal("load_b")

                        if  shared_memory.arm2_end_flag == True and shared_memory.arm2_end_message == "IDLE":
                            if  shared_memory.burger1_end_flag == True and shared_memory.burger1_end_message == "IDLE":
                                self.get_logger().info("\033[1;32mSingle 동작 정상 완료\033[0m")
                            else:
                                self.get_logger().info("\033[1;31mburger1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")
                        else:
                            self.get_logger().info("\033[1;31marm2 동작에 실패했습니다. 다시 시작해주세요.\033[0m")
                else:
                    self.get_logger().info("\033[1;31mburger2 동작에 실패했습니다. 다시 시작해주세요.\033[0m")
            else:
                self.get_logger().info("\033[1;31marm1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")

        else:
            self.get_logger().info("\033[1;31mburger1 동작에 실패했습니다. 다시 시작해주세요.\033[0m")