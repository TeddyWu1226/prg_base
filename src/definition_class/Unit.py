import abc
from abc import ABC
from dataclasses import dataclass, field
from typing import Union

from definition_class import Skill
from definition_class.Skill import ActiveSkill, NoneSkill
from definition_class.Status import EffectStatus
from definition_class.ValueCurve import defend_curve


@dataclass
class UnitInfo:
    name: str
    race: str
    hp_limit: int = 0
    sp_limit: int = 0
    level: int = 1
    ad_attack: int = 0
    ap_attack: int = 0
    ad_df: int = 0
    ap_df: int = 0
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
        self.hp_limit = info.hp_limit
        self.sp_limit = info.sp_limit
        self.hp = info.hp_limit
        self.sp = info.sp_limit
        self.status = info.status
        self.ad_attack = info.ad_attack
        self.ap_attack = info.ap_attack
        self.ad_df = info.ad_df
        self.ap_df = info.ap_df
        self.skills = info.skills
        self.passive = info.passive
        self.is_alive = True
        self.default_action_point = info.default_action_point
        self.action_point = info.default_action_point
        self.is_stop = False

    def learn(self, skill: Skill):
        self.skills.append(skill)

    def show_info(self):
        print('-------------')
        print(f'名稱:{self.name} {"" if self.is_alive else "(死亡)"}')
        print(f'等級:{self.level}')
        print(f'HP:{self.hp} / {self.hp_limit}')
        print(f'SP:{self.sp} / {self.sp_limit}')
        print(f'攻擊力:{self.ad_attack}')
        print(f'魔力:{self.ap_attack}')
        print(f'當前狀態:{",".join([status.name for status in self.status]) if self.status else "無"}')
        print('-------------')

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
        return self.working_skill(self.skills[self.skills.index(key)])

    def __str__(self):
        return self.name

    @property
    def action(self):
        """
        動作判定，消耗行動值
        :return:
        """
        self.reduce_action_point()
        return self

    def working_skill(self, skill: ActiveSkill):
        skill.set_speller(self)
        return skill

    def set_status(self, effect: Union[list, EffectStatus]):
        if isinstance(effect, list):
            self.status.extend(effect)
        elif isinstance(effect, EffectStatus):
            self.status.append(effect)

    def value_change(self, value: int, colum: str):
        if colum == 'hp':
            self.hp += value
            if self.hp > self.hp_limit:
                self.hp = self.hp_limit
        elif colum == 'sp':
            self.sp += value
            if self.sp > self.sp_limit:
                self.sp = self.sp_limit
        elif colum == 'level':
            self.level += value

        if self.hp <= 0:
            self.before_die()
            self.dead()

    def value_percent_change(self, percent: float, colum=str):
        if colum == 'hp':
            self.hp += (percent * self.hp_limit)
            if self.hp > self.hp_limit:
                self.hp = self.hp_limit
        elif colum == 'sp':
            self.sp += (percent * self.sp_limit)
            if self.sp > self.sp_limit:
                self.sp = self.sp_limit
        if self.hp <= 0:
            self.before_die()
            self.dead()

    def dead(self):
        print(f'{self.name} 死亡!')
        self.is_alive = False
        self.is_stop = True

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

    def attack(self, target):
        damage = self.ad_attack
        print(f'{self.name} 攻擊 {target.name}!')
        target.attacked(attacker=self, damage=damage)

    def attacked(self, attacker, damage, _type='ad'):
        cause_damage = damage - defend_curve(self.ad_df if _type == 'ad' else self.ap_df)
        cause_damage = cause_damage if cause_damage > 0 else 0
        print(f'造成了 {cause_damage} 傷害!')
        self.value_change(-cause_damage, 'hp')
        if self.is_alive:
            print(f'{self.name} 剩下 {self.hp} 生命')
        else:
            give_exp = int(round(self.level ** 1.2 * 75, 0)) + 25
            print(f'{attacker.name} 擊敗了 {self.name}, 獲得了 {give_exp} 經驗!')
            if callable(attacker.get_exp):
                attacker.get_exp(give_exp)

    @abc.abstractmethod
    def before_die(self):
        pass
