from abc import ABC, abstractmethod


class Observed(ABC):
    def __init__(self, value):
        self.value = value
        self.original_value = self.value

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    # 運算
    def __add__(self, other):
        if isinstance(other, ObVar):
            return self.value + other.value
        else:
            return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __floordiv__(self, other):
        return self.value // other

    # 賦值
    def __isub__(self, other):
        self.value -= other
        self.check()
        return self

    def __iadd__(self, other):
        self.value += other
        self.check()
        return self

    def __neg__(self):
        self.value = -self.value
        self.check()
        return self

    def set(self, value):
        self.value = value
        self.check()

    def check(self):
        if self.value != self.original_value:
            self.notify()
        self.original_value = self.value

    @abstractmethod
    def notify(self) -> None:
        pass


class ObVar(Observed):
    """
    被監聽的變數
    value: 變數值
    event: 監聽觸發事件
    **kwarg: 事件變數(參數=值)
    """

    def __init__(self, value, event: callable, **kwargs):
        super().__init__(value)
        self.event = event
        self.param = kwargs

    def notify(self):
        if not callable(self.event):
            return
        else:
            return self.event(**self.param)
