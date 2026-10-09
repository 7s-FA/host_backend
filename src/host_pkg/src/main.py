import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor
from burger1_node import Burger1ActionClient
from burger2_node import Burger2ActionClient
from waffle_node import waffleActionClient

from arm1_node import Arm1ActionClient
from arm2_node import Arm2ActionClient
from arm3_node import Arm3ActionClient

from web_node import WebDataPase

from control import RobotController

def main(args=None):
    rclpy.init(args=args)

    WebDataPaser = WebDataPase()

    Burger1Act = Burger1ActionClient()
    Burger2Act = Burger2ActionClient()
    WaffleAct = waffleActionClient()

    Arm1Act = Arm1ActionClient()
    Arm2Act = Arm2ActionClient()
    Arm3Act = Arm3ActionClient()

    Controller = RobotController(Burger1Act, Burger2Act, WaffleAct, Arm1Act, Arm2Act, Arm3Act) # waffle 까지 추가해서 해줘야 함 우선 테스트를 위해 버거 1,2만 

    # Burger1Act.send_goal(command="move_forward", speed=1.5)

    executor = MultiThreadedExecutor()
    executor.add_node(WebDataPaser)

    executor.add_node(Burger1Act)
    executor.add_node(Burger2Act)
    executor.add_node(WaffleAct)

    executor.add_node(Arm1Act)
    executor.add_node(Arm2Act)
    executor.add_node(Arm3Act)

    executor.add_node(Controller)
    # 핵심 수정: send_goal을 별도 스레드에서 실행하여 main이 멈추지 않고 즉시 executor.spin()으로 진입하게 함

    try:
        executor.spin()
    except KeyboardInterrupt:
        # WebDataPaser.send_status_to_web() # 끝날때 이부분 실행해줘야 되고 이앞에서 플래그 같을걸로 web쪽에 데이터 끝낸다는걸 알려줘야 함.

        Burger1Act.destroy_node()
        Burger2Act.destroy_node()
        WaffleAct.destroy_node()

        Arm1Act.destroy_node()
        Arm2Act.destroy_node()
        Arm3Act.destroy_node()

        WebDataPaser.destroy_node()
        Controller.destroy_node()
        rclpy.shutdown()
        pass

if __name__ == '__main__':
    main()