from EffectList import EffectDizzy
from definition_class import ActiveSkill
from definition_class.Skill import SkillVM, TargetType


class FireBall(ActiveSkill):
    def __init__(self, damage=50, cost_sp=50):
        fireball_vm = SkillVM(code='FIREBALL', name='火球術', text='施展火球術，擊暈敵人2秒', damage=damage,
                              extra_effect=[EffectDizzy(duration=2)])
        super().__init__(cost_sp=cost_sp, skill_vm=fireball_vm)


class HealingMagic(ActiveSkill):
    def __init__(self, heal=50, cost_sp=20):
        fireball_vm = SkillVM(code='HEALING', name='治癒術', text='治療目標', heal=heal,
                              target_type=TargetType.Self.value)
        super().__init__(cost_sp=cost_sp, skill_vm=fireball_vm)
