import asyncio
from definition_class import Clock
from SkillList import FireBall, HealingMagic
from UnitList import Slime, Human

if __name__ == '__main__':
    print('---角色建立---')
    mage = Human()
    mage.learn(FireBall(damage=100, cost_sp=25))
    slime = Slime(hp_limit=250, level=1)
    slime.learn(HealingMagic(heal=50, cost_sp=20))

