# coding = utf-8

from taskinterface import taskinterface
from plane_main import PlaneGame
import const

const.PLANEWAR_NAME = 'plane war'

class task_planewar(taskinterface):
    
    def __init__(self) -> None:
        self._name = const.PLANEWAR_NAME
        self._tasktype = 'game'
        self._parameter = ''

        super().__init__()
    
    def _fupdateparameter(self) -> str:
        pass

    def _fconvertparmaeter(self, parameter: str) -> None:
        pass
    
    def _fcheckparmaeter(self) -> bool:
        return True

    def run(self) -> int:
        # 创建游戏对象
        game = PlaneGame()

        # 启动游戏
        game.start_game()


    def opensetup(self) -> int:
        return 0

    def getname(self) -> str:
        return self._name

    def gettype(self) -> str:
        return self._tasktype

    def getparameter(self) -> str:
        return self._parameter

    def setparameter(self, parameter: str) -> int:
        self._parameter = parameter
        if len(parameter) > 0:
            return self._fconvertparmaeter(parameter)
        return 0

    def getpercent(self) -> int:
        return self._percent
