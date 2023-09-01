from EffectList import EffectDizzy, EffectBurn
from definition_class import ActiveSkill
from definition_class.Skill import SkillVM, TargetType


# 單體技能
class FireBall(ActiveSkill):
    def __init__(self, level):
        fireball_vm = SkillVM(code='FIREBALL',
                              name='火球術',
                              text='施展火球術，造成單體 {damage} 傷害，並造成{effects}效果',
                              damage_base=20,
                              upgrade_value=30,
                              sp_cost=40,
                              upgrade_cost_value=10,
                              extra_effect=[EffectBurn()])
        super().__init__(level=level, skill_vm=fireball_vm)


# 範圍技能

# 自我施展技能
class HealingMagic(ActiveSkill):
    def __init__(self, heal=50, cost_sp=20):
        fireball_vm = SkillVM(code='HEALING', name='治癒術', text='治療目標', heal_base=heal,
                              target_type=TargetType.Self.value)
        super().__init__(cost_sp=cost_sp, skill_vm=fireball_vm)
