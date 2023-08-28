import abc
from abc import ABC
from dataclasses import dataclass, field

from definition_class import Skill
from definition_class.Skill import ActiveSkill, NoneSkill
from definition_class.Status import EffectStatus


@dataclass
class UnitInfo:
    name: str
    race: str
    hp_limit: int = 0
    sp_limit: int = 0
    level: int = 1
    speed: int = 0
    attack: int = 0
    defend: int = 0
    status: list = field(default_factory=list)
    skills: list = field(default_factory=list)
    passive: list = field(default_factory=list)
    default_action_point: int = 1

    def __getitem__(self, key):
        return getattr(self, key)


class Unit(ABC):
    def __init__(self, info: UnitInfo):

        self.name = info.name
        self.level = info.level
        self.race = info.race
        self.hp = info.hp_limit
        self.sp = info.sp_limit
        self.status = info.status
        self.attack = info.attack
        self.defend = info.defend
        self.speed = info.speed
        self.skills = info.skills
        self.passive = info.passive
        self.is_alive = True
        self.default_action_point = info.default_action_point
        self.action_point = info.default_action_point
        self.is_stop = False

    def __getitem__(self, key):
        return self.info[key]

    def learn(self, skill: Skill):
        self.skills.append(skill)

    def __getattr__(self, key):
        if self.is_stop:
            print(f'{self.name} 無法行動')
            return NoneSkill()
        if self.action_point <= 0:
            print(f'{self.name} 行動值耗盡，無法行動')
            return NoneSkill()
        if not self.is_alive:
            return NoneSkill()
        if key not in self.skills:
            print(f'{self.name} 沒有 {key} 技能')
            return NoneSkill()
        return self.action.working_skill(self.skills[self.skills.index(key)])

    @property
    def action(self):
        """
        動作判定，消耗行動值
        :return:
        """
        self.reduce_action_point()
        return self

    def working_skill(self, skill: ActiveSkill):
        skill.setSpeller(self)
        return skill

    def setStatus(self, effect: EffectStatus):
        if isinstance(effect, list):
            self.status.extend(effect)
        elif isinstance(effect, EffectStatus):
            self.status.append(effect)

    def value_change(self, value: int, colum=str):
        if colum == 'hp':
            self.hp += value
        elif colum == 'sp':
            self.sp += value
        elif colum == 'level':
            self.level += value

        if self.hp <= 0:
            self.before_die()
            self.kill()

    def kill(self):
        print(f'{self.name} 死亡')
        self.is_alive = False

    def add_action_point(self):
        self.action_point += 1
        self.watch_action_point()

    def reduce_action_point(self):
        if self.action_point > 0:
            self.action_point -= 1
        else:
            self.action_point = 0

    def restore_action_point(self):
        self.action_point = self.default_action_point

    def clear_action_point(self):
        self.action_point = 0

    def round_pass(self):
        pass

    @abc.abstractmethod
    def before_die(self):
        pass
