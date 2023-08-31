import asyncio
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
    damage: int = 0  # 傷害
    heal: int = 0  # 治療
    extra_effect: list = field(default_factory=list)  # 附加效果
    target_type: int = TargetType.Single.value  # 技能目標數量


class ActiveSkill:
    def __init__(self, skill_vm: SkillVM, cost_sp: int = 0, cost_hp: int = 0, spell_wait=0):
        self.targets: Union[List[Unit], Unit, None] = None
        self.speller: Unit = None
        self.cost_hp = cost_hp
        self.cost_sp = cost_sp
        self.spell_wait = spell_wait
        self.skill_vm = skill_vm

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

    async def waiting(self):
        await asyncio.sleep(self.spell_wait)
        return True

    def spell(self):
        self.speller.value_change(-self.cost_sp, 'sp')
        print(f'{self.speller.name} 施展了 {self.skill_vm.name}')
        for target in self.targets:
            if self.skill_vm.damage:
                target.set_status(self.skill_vm.extra_effect)
                target.attacked(attacker=self.speller, damage=self.skill_vm.damage, _type='ap')

            if self.skill_vm.heal:
                print(f'{target.name} 回復了 {self.skill_vm.heal} 生命')
                target.set_status(self.skill_vm.extra_effect)
                target.value_change(self.skill_vm.heal, 'hp')

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
