import time

class SharedState:
    def __init__(self):

        self.start_flag = False
        self.quantity = 0
        self.product = ""

        self.remaining_material_A = 2
        self.remaining_material_B = 2

        #Robot - burger1
        self.burger1_x_axis = 0.0
        self.burger1_y_axis = 0.0
        self.burger1_theta = ""
        self.burger1_feedback_msg = ""


        self.burger1_success = False
        self.burger1_end_message = ""
        self.burger1_end_flag = False

        #Robot - burger2
        self.burger2_x_axis = 0.0
        self.burger2_y_axis = 0.0
        self.burger2_theta = ""
        self.burger2_feedback_msg = ""

        self.burger2_success = False
        self.burger2_end_message = ""
        self.burger2_end_flag = False

        #Robot - waffle
        self.waffle_x_axis = 0.0
        self.waffle_y_axis = 0.0
        self.waffle_theta = ""
        self.waffle_feedback_msg = ""

        self.waffle_success = False
        self.waffle_end_message = ""
        self.waffle_end_flag = False


        #arm - arm1
        self.arm1_feedback_msg = ""

        self.arm1_success = False
        self.arm1_end_message = ""
        self.arm1_end_flag = False

        #arm - arm2
        self.arm2_feedback_msg = ""

        self.arm2_success = False
        self.arm2_end_message = ""
        self.arm2_end_flag = False

        #arm - arm3
        self.arm3_feedback_msg = ""

        self.arm3_success = False
        self.arm3_end_message = ""
        self.arm3_end_flag = False

# 전역에서 쓸 수 있는 단일 공유 객체 생성
shared_memory = SharedState()