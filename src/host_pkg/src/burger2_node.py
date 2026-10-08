from burger_base import BurgerActionClient

class Burger2ActionClient(BurgerActionClient):
    def __init__(self):
        super().__init__('M2', 'burger2') # 수신을 /M2/data 로 함
