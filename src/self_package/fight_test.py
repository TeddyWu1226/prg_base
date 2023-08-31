from UnitList import Slime
from definition_class import Hero
from definition_class.Stage import FightStage

if __name__ == '__main__':
    hero = Hero(name='ted', _str=10, _agi=10, _int=10)
    slime1 = Slime(level=1)
    slime2 = Slime(level=2)
    test_stage = FightStage([hero], [slime1, slime2])