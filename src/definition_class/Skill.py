from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

from definition_class import Unit


class TargetType(Enum):
    Self = 0
    Single = 1
    Multiple = 2
    Range = 3


@dataclass
class SkillVM:
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
    def __init__(self, skill_vm: SkillVM, level: int = 0):
        self.targets: Union[List[Unit], Unit, None] = None
        self.speller: Unit = None
        self.skill_vm = skill_vm
        self.level = level
        self.cost_hp = self.skill_vm.hp_cost + self.skill_vm.upgrade_cost_value * level
        self.cost_sp = self.skill_vm.sp_cost + self.skill_vm.upgrade_cost_value * level

    @property
    def code(self):
        return self.skill_vm.code

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
        for target in self.targets:
            if self.skill_vm.damage_base:
                damage = self.skill_vm.damage_base + self.skill_vm.upgrade_value * self.level
                target.set_status(self.skill_vm.extra_effect)
                target.attacked(attacker=self.speller, damage=damage, _type=self.skill_vm.type)

            if self.skill_vm.heal_base:
                heal = self.skill_vm.heal_base + self.skill_vm.upgrade_value * self.level
                print(f'{target.name} 回復了 {heal} 生命')
                target.set_status(self.skill_vm.extra_effect)
                target.value_change(heal, 'hp')

    def show_info(self):
        print('~~~~~~~~~')
        print(f'{self.skill_vm.name} (等級{self.level})  消耗:{self.cost_sp}SP')
        print(self.skill_vm.text.format(damage=self.skill_vm.damage_base + self.skill_vm.upgrade_value * self.level,
                                        heal=self.skill_vm.damage_base + self.skill_vm.upgrade_value * self.level,
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
    def __init__(self):
        fireball_vm = SkillVM(code='Non', name='')
        super().__init__(skill_vm=fireball_vm)
