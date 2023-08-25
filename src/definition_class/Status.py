import datetime
from abc import ABC, abstractmethod


class EffectStatus(ABC):
    def __init__(self, name: str, duration=0.0, is_permanent=False):
        self._name = name
        self.start_time = datetime.datetime.now()
        self.is_permanent = is_permanent
        if is_permanent:
            self.end_time = None
        else:
            self.end_time = self.start_time + datetime.timedelta(seconds=duration)

    @property
    def name(self):
        return self._name

    @property
    def rd(self):
        if self.is_permanent:
            return 99999
        elif datetime.datetime.now() > self.end_time:
            return 0
        else:
            return (self.end_time - datetime.datetime.now()).seconds

    def destroy(self):
        self.beforeDestroy()
        del self

    @abstractmethod
    def getEffectText(self) -> str:
        return ''

    @abstractmethod
    def getEffect(self) -> dict:
        return {}

    @abstractmethod
    def beforeDestroy(self):
        pass


class EffectDizzy(EffectStatus):

    def __init__(self, duration=0.0, is_permanent=False):
        super().__init__('Dizzy', duration, is_permanent)

    def getEffectText(self) -> str:
        return '不能採取任何動作'

    def getEffect(self) -> dict:
        return {'style': 'negative'}

    def beforeDestroy(self):
        pass
