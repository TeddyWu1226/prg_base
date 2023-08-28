import datetime
from abc import ABC, abstractmethod


class EffectStatus(ABC):
    def __init__(self, name: str, duration=0, is_permanent=False):
        self._name = name
        self.start_time = datetime.datetime.now()
        self.is_permanent = is_permanent
        if is_permanent:
            self.current_duration = 999
        else:
            self.current_duration = duration

    def __repr__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def check_remain(self):
        print(f'{self._name} 執行了check_remain')
        self.reduce_duration()
        if self.current_duration <= 0:
            self.before_destroy()
            self.current_duration = 0
        return self.current_duration

    @abstractmethod
    def get_effect_text(self) -> str:
        return ''

    @abstractmethod
    def get_effect(self) -> dict:
        return {}

    def reduce_duration(self):
        self.current_duration -= 1

    @abstractmethod
    def before_destroy(self):
        pass


class EffectList:
    def __init__(self, effect_list: list):
        self.effect_list = effect_list

    def __repr__(self):
        return self.effect_list

    def add(self, effect: EffectStatus):
        if isinstance(effect, EffectStatus):
            self.effect_list.append(effect)
        elif isinstance(effect, list):
            self.effect_list.extend(effect)

    def check_remain(self):
        self.effect_list = list(filter(lambda effect: effect.check_remain() != 0, self.effect_list))
