from burger_base import BurgerActionClient

class Burger1ActionClient(BurgerActionClient):
    def __init__(self):
        super().__init__('M1', 'burger1') # 수신을 /M1/data 로 함
