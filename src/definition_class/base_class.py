"""
基類，所有抽象化的class放在這裡
避免循環引入的問題
"""
import datetime
import abc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Type, List
from definition_class.ValueCurve import defend_curve
from self_package import ObVar


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
    """
    單位
    """

    def __init__(self, info: UnitInfo):

        self.name = info.name
        self.level = info.level
        self.race = info.race
        self.hp_limit = info.hp_limit
        self.sp_limit = info.sp_limit
        self.hp = info.hp_limit
        self.sp = info.sp_limit
        self.status = EffectList(info.status)
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

    def learn(self, skill):
        self.skills.append(skill)

    def show_info(self):
        print('-------------')
        print(f'名稱:{self.name} {"" if self.is_alive else "(死亡)"}')
        print(f'等級:{self.level}')
        print(f'HP:{self.hp} / {self.hp_limit}')
        print(f'SP:{self.sp} / {self.sp_limit}')
        print(f'攻擊力:{self.ad_attack}')
        print(f'魔力:{self.ap_attack}')
        print(f'當前狀態:{self.status}')
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

    def working_skill(self, skill):
        skill.set_speller(self)
        return skill

    def set_status(self, effect: Union[list, Type['EffectStatus']]):
        self.status.add(effect)

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

    def attacked(self, attacker, damage, _type='ad'):  # type=ad(物理),ap(魔法),dir(真實)
        if _type != 'dir':
            cause_damage = damage - defend_curve(self.ad_df if _type == 'ad' else self.ap_df)
        else:
            cause_damage = damage
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

    def before_round_check_status(self):
        self.status.at_round_before_working()

    def after_round_check_status(self):
        self.status.at_round_after_working()


class EffectStatus(ABC):
    """
    效果(狀態)
    """

    def __init__(self, name: str, duration=0, is_permanent=False, is_stacked=False):
        self._name = name
        self.is_stacked = is_stacked
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

    def set_giver(self, unit: Union[Unit] = None):
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
    """
    效果狀態列
    """

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

    def _check_is_repeat_effect(self, effect):
        print(effect)
        print(set(self.effect_list))
        pass

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


class TargetType(Enum):
    """目標類型"""
    Self = 0
    Single = 1
    Multiple = 2
    Range = 3


@dataclass
class SkillVM:
    """
    技能VM
    """
    code: str  # 技能代號
    name: str  # 技能名稱
    text: str = None  # 技能敘述
    type: str = 'ap'  # 傷害類型
    damage_base: int = 0  # 傷害
    heal_base: int = 0  # 治療
    upgrade_value: float = 0  # 技能等級提升時的數值加乘
    sp_cost: int = 0  # 耗費法力
    hp_cost: int = 0  # 耗費生命
    upgrade_cost_value: int = 0  # 技能等級提升時的耗費加乘
    limit_level: int = 3  # 技能等級上限
    extra_effect: list = field(default_factory=list)  # 附加效果
    target_type: int = TargetType.Single.value  # 技能目標數量


class ActiveSkill:
    """
    主動技能
    """

    def __init__(self, skill_vm: SkillVM, level: int = 0):
        self.targets: Union[List[Unit], Unit, None] = None
        self.speller: Union[Unit, None] = None
        self.skill_vm = skill_vm
        self.level = ObVar(level, self.update_setting)
        self.cost_hp = 0
        self.cost_sp = 0
        self.total_damage = 0
        self.total_heal = 0
        self.update_setting()

    @property
    def code(self):
        return self.skill_vm.code

    def update_setting(self):
        self.cost_hp = self.skill_vm.hp_cost + self.level * self.skill_vm.upgrade_cost_value
        self.cost_sp = self.skill_vm.sp_cost + self.level * self.skill_vm.upgrade_cost_value
        self.total_damage = self.skill_vm.damage_base + self.skill_vm.upgrade_value * int(self.level)
        self.total_heal = self.skill_vm.damage_base + self.skill_vm.upgrade_value * int(self.level)

    def upgrade(self, point=1):
        self.level += point

    def set_speller(self, speller):
        self.speller = speller

    def set_target(self, target: list):
        if target:
            self.targets = list(filter(lambda unit: unit.is_alive, target))
        else:
            self.targets = []
        if self.skill_vm.target_type == TargetType.Self.value:
            if len(self.targets) > 0:
                print('無效的目標設定')
                return False
            else:
                self.targets = [self.speller]
        elif self.skill_vm.target_type == TargetType.Single.value:
            if len(self.targets) != 1:
                print('無效的目標設定')
                return False
        elif self.skill_vm.target_type == TargetType.Multiple.value:
            if len(self.targets) == 0:
                print('無效的目標設定')
                return False

        return True

    def spell(self):
        self.speller.value_change(-self.cost_sp, 'sp')
        print(f'{self.speller.name} 施展了 {self.skill_vm.name}')
        for _effect in self.skill_vm.extra_effect:
            _effect.set_giver(self.speller)

        for target in self.targets:
            if self.skill_vm.damage_base:
                damage = self.skill_vm.damage_base + self.skill_vm.upgrade_value * int(self.level)
                target.set_status(self.skill_vm.extra_effect)
                target.attacked(attacker=self.speller, damage=damage, _type=self.skill_vm.type)

            if self.skill_vm.heal_base:
                heal = int(self.skill_vm.heal_base + self.skill_vm.upgrade_value * int(self.level))
                print(f'{target.name} 回復了 {heal} 生命')
                target.set_status(self.skill_vm.extra_effect)
                target.value_change(heal, 'hp')

    def show_info(self):
        print('~~~~~~~~~')
        print(f'{self.skill_vm.name} (等級{self.level})  消耗:{self.cost_sp}SP')
        print(
            self.skill_vm.text.format(damage=self.total_damage,
                                      heal=self.total_heal,
                                      effects=','.join([effect.name for effect in self.skill_vm.extra_effect])))
        print('~~~~~~~~~')

    def before_spell(self):
        if not self.speller:
            print('錯誤，找不到施法者')
            return False
        if self.speller.sp < self.cost_sp:
            print(f'{self.speller.name} 魔力不足，無法施展 {self.skill_vm.name}')
            return False
        elif self.speller.hp < self.cost_hp:
            print(f'{self.speller.name} 生命不足，無法施展 {self.skill_vm.name}')
            return False
        else:
            return True

    def __call__(self, *args):
        if self.skill_vm.code == 'Non':
            return
        if not self.before_spell():
            return
        is_target_success = self.set_target(list(args))
        if is_target_success:
            is_spell_success = True
            if is_spell_success:
                self.spell()

    def __eq__(self, other):
        return self.skill_vm.code == other

    def __repr__(self):
        return str(self.skill_vm.code)

    def __str__(self):
        return self.skill_vm.name


class NoneSkill(ActiveSkill):
    """
    無技能
    """

    def __init__(self):
        skill_vm = SkillVM(code='Non', name='')
        super().__init__(skill_vm=skill_vm)
