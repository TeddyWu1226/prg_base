import datetime
from abc import ABC, abstractmethod
from typing import Union, List

from definition_class import Unit


class EffectStatus(ABC):
    def __init__(self, name: str, duration=0, is_permanent=False):
        self._name = name
        self.start_time = datetime.datetime.now()
        self.is_permanent = is_permanent
        self.default_duration = duration
        self.owner: Union[Unit, None] = None
        self.giver: Union[Unit, None] = None
        if is_permanent:
            self.current_duration = 999
        else:
            self.current_duration = duration

    def __repr__(self):
        return self._name

    def set_owner(self, unit: Unit):
        self.owner = unit

    def set_giver(self, unit: Unit = None):
        if unit:
            self.giver = unit

    @property
    def name(self):
        return self._name

    def reduce_duration(self):
        if not self.is_permanent:
            self.current_duration -= 1

    @abstractmethod
    def at_round_before(self):
        """
        回合開始時觸發
        :return:
        """
        pass

    @abstractmethod
    def at_round_after(self):
        """
        回合結束時觸發
        :return:
        """
        pass

    @abstractmethod
    def trigger(self):
        """
        觸發鉤子
        :return:
        """
        pass


class EffectList:
    def __init__(self, effect_list: List[EffectStatus]):
        self.owner: Union[Unit, None] = None
        self.effect_list = effect_list

    def __repr__(self):
        return self.effect_list

    def __str__(self):
        return ",".join([effect.name for effect in self.effect_list]) if self.effect_list else "無"

    def set_owner(self, unit: Unit):
        self.owner = unit

    def add(self, effect: Union[EffectStatus, List[EffectStatus]]):
        if not effect:
            return
        if isinstance(effect, EffectStatus):
            effect.set_owner(self.owner)
            self.effect_list.append(effect)
        elif isinstance(effect, list):
            for _effect in effect:
                _effect.set_owner(self.owner)
                self.effect_list.append(_effect)

    def update_duration(self):
        for _effect in self.effect_list:
            _effect.reduce_duration()
        self.effect_list = list(filter(lambda effect: effect.current_duration > 0, self.effect_list))

    def at_round_before_working(self):
        for _effect in self.effect_list:
            _effect.at_round_before()

    def at_round_after_working(self):
        for _effect in self.effect_list:
            _effect.at_round_after()
        self.update_duration()
