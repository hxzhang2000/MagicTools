# coding = utf-8
from abc import ABCMeta, abstractmethod

class taskinterface(object):
    '任务接口类'
    __metaclass__ = ABCMeta     #指定这是一个抽象类

    _name : str
    _tasktype : str
    _parameter : str
    _percent : int

    @abstractmethod
    def _fupdateparameter(self) -> str:
        """内部函数，用于将保存的参数，转换为json字符串，并更新_parameter
        
        Returns:
            str: 转换后的json字符串
        """        
        pass

    @abstractmethod
    def _fconvertparmaeter(self, parameter: str) -> None:
        """内部函数，用于转换输入的参数字符串

        Args:
            parameter (str): 传入的json字符串
        """        
        pass
    
    @abstractmethod
    def _fcheckparmaeter(self) -> bool:
        """内部函数，运行前检测各项参数是否合法

        Returns:
            bool: 是/否
        """        
        pass

    @abstractmethod
    def run(self) -> int:
        """运行此插件

        Returns:
            int: 成功：0，其他：错误代码
        """        
        pass

    @abstractmethod
    def opensetup(self) -> int:
        """打开此插件的设置窗口

        Returns:
            int: 成功：0，其他：错误代码
        """        
        pass

    @abstractmethod
    def getname(self) -> str:
        """获取插件名称

        Returns:
            str: 此插件名称
        """        
        pass

    @abstractmethod
    def gettype(self) -> str:
        """获取插件类型

        Returns:
            str: 此插件类型
        """        
        pass

    @abstractmethod
    def getparameter(self) -> str:
        """获取已经配置的插件参数，未配置为‘’

        Returns:
            str: 插件参数
        """        
        pass

    @abstractmethod
    def setparameter(self, parameter: str) -> int:
        """设置插件参数

        Args:
            parameter (str): 插件参数,json格式
        Returns:
            int: 成功：0，其他：错误代码
        """        
        pass

    @abstractmethod
    def getpercent(self) -> int:
        """获取运行进度百分比

        Returns:
            int: 运行进度百分比(0-100)
        """        
        pass
