import rclpy
import threading
import time
from rclpy.node import Node
from shared_data import shared_memory

# 로봇 한 대의 한 동작(goal)이 끝나기를 기다리는 최대 시간. 로봇 Action 서버의 mission_timeout_s(600s)보다
# 조금 길게 두어, 정상적인 시간 초과는 로봇이 먼저 ERROR 로 보고하게 한다. 로봇이 꺼지거나 응답이
# 끊겨도 흐름이 영원히 멈추지 않도록 하는 마지막 안전장치.
GOAL_TIMEOUT_SEC = 660.0
RESTART_RETRIES = 5 # RESTART 는 정지 상태를 0.3초 이상 확인해야 성공하므로 몇 번 재시도
RESTART_RETRY_SEC = 1.0

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

        # 로봇 흐름은 별도 스레드에서 돌린다. 타이머 콜백 안에서 기다리면 주행 중에는 정지 입력을 볼 수 없다.
        self._worker = None
        self._abort = threading.Event()

        self.timer = self.create_timer(0.2, self.controlRobot) # print 문 빼고 나중에 0.1초로 바꾸자
        self.get_logger().info('RobotController 노드가 시작되었습니다.')

    def controlRobot(self):

        if  self.old_start_flag == shared_memory.start_flag:
            # no operate
            self.get_logger().info("정상 종료 : 이전 상태와 동일한 상태 입력 / 현 동작 유지", throttle_duration_sec=1.0)
        elif shared_memory.start_flag == True:
            if self._worker is not None and self._worker.is_alive():
                # 이전 흐름이 정리되는 중이면 old_start_flag 를 바꾸지 않고 다음 주기에 다시 시도
                self.get_logger().info("이전 동작 정리 중 : 다음 주기에 시작 재시도", throttle_duration_sec=1.0)
                return

            self.old_start_flag = True
            self.get_logger().info("\033[1;31m로봇 동작 시작\033[0m")

            multi = shared_memory.quantity >= 2
            self._abort.clear()
            self._worker = threading.Thread(target=self._runFlow, args=(multi,), daemon=True)
            self._worker.start()
        else:
            self.old_start_flag = False
            self.get_logger().info("\033[1;31m로봇 정지\033[0m")
            self._stopFlow()

    def _stopFlow(self):
        # 진행 중인 흐름이 다음 로봇으로 넘어가지 않게 중단하고, 이동 중인 로봇에는 EMER_STOP 을 보낸다.
        if self._worker is not None and self._worker.is_alive():
            self._abort.set()
            self._emergencyStop()

    def _emergencyStop(self):
        for name, robot in (("burger1", self.burger1), ("burger2", self.burger2)):
            if robot.moving:
                # 응답을 기다리는 동안 타이머가 막히지 않도록 별도 스레드에서 보낸다.
                threading.Thread(target=self._sendEmergencyStop, args=(name, robot), daemon=True).start()

    def _sendEmergencyStop(self, name, robot):
        robot.needs_restart = True # EMER_STOP 이 성공해도 로봇은 정지 래치 상태가 된다
        if robot.send_control("EMER_STOP"):
            self.get_logger().info(f"{name} 비상정지 완료")
        else:
            # 정지를 확인하지 못했으면 최소한 goal 취소라도 요청한다
            self.get_logger().error(f"{name} 비상정지 확인 실패 : goal 취소 요청")
            robot.cancel_goal()

    def _runFlow(self, multi):
        try:
            if multi:
                self.controlMultiRobot()
            else:
                self.controlSingleRobot()
        except Exception as error:
            self.get_logger().error(f"로봇 동작 흐름 오류: {error}")

    def _prepareRobot(self, name, robot):
        """이전 동작이 정상 종료되지 않았으면 RESTART 로 정지 래치를 먼저 해제한다 (이동을 재개하지는 않음)."""
        if not robot.needs_restart:
            return True

        self.get_logger().info(f"{name} 이전 동작이 정상 종료되지 않음 : RESTART 로 정지 해제")
        for attempt in range(RESTART_RETRIES):
            if self._abort.is_set():
                return False
            if robot.send_control("RESTART"):
                robot.needs_restart = False
                return True
            time.sleep(RESTART_RETRY_SEC)
        self.get_logger().error(f"{name} RESTART 실패 : 로봇이 정지 상태인지, 서버가 살아 있는지 확인 필요")
        return False

    def _waitForRobot(self, name, robot, command, speed):
        """goal 을 보내고 결과를 기다린다. 성공(IDLE)이면 True, 실패/중단/시간 초과면 False."""
        if not self._prepareRobot(name, robot):
            return False

        if not robot.send_goal(command, speed):
            self.get_logger().error(f"{name} 동작 시작 실패 : Action 서버에 연결할 수 없음")
            return False

        end_flag = f"{name}_end_flag"
        deadline = time.monotonic() + GOAL_TIMEOUT_SEC
        while not getattr(shared_memory, end_flag):
            if self._abort.is_set():
                self.get_logger().info(f"{name} 동작 중단 : 정지 입력")
                return False # EMER_STOP 은 _stopFlow 가 이미 보냄
            if time.monotonic() > deadline:
                self.get_logger().error(f"{name} 동작 시간 초과 ({GOAL_TIMEOUT_SEC:.0f}s) : 로봇 응답 없음 → 비상정지")
                robot.needs_restart = True
                threading.Thread(target=self._sendEmergencyStop, args=(name, robot), daemon=True).start()
                return False
            time.sleep(0.1)

        setattr(shared_memory, end_flag, False)

        success = getattr(shared_memory, f"{name}_success")
        message = getattr(shared_memory, f"{name}_end_message")
        if success == True and message == "IDLE":
            return True

        self.get_logger().warning(f"{name} 동작 실패 : success={success}, message=\"{message}\"")
        return False

    def controlSingleRobot(self):
        self.get_logger().info("Single Robot Flow - only Burger1 moves")
        # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경
        if self._waitForRobot("burger1", self.burger1, "GO_TO_MAT", 99.0):
            self.get_logger().info("ENDENDENDENDENDENDENDENDENDENDEND")

    def controlMultiRobot(self):
        self.get_logger().info("Multi Robot Flow - Both Robotes move")
        # 속도값 변수로 나중에 변경해줘야 함. -> Web 에서 받아오게끔 변경
        if self._waitForRobot("burger1", self.burger1, "GO_TO_MAT", 99.0):
            self._waitForRobot("burger2", self.burger2, "GO_TO_REST", 99.0)

        # Test를 위해 Burger 1 -> 재료 , Burger 2 대기 장소 까지 이동만 시킴
