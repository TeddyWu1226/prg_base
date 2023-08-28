from enum import Enum
from Setting import LANGUAGE


class Round:
    def __init__(self, _type):
        self.type = _type.value

    def __repr__(self):
        return self.type

    def __str__(self):
        return str(self.type)

    def __iadd__(self, other):
        self.type += other
        return self

    def __eq__(self, other):
        return self.type == other

    @property
    def name(self):
        return globals()[f'FIGHT_ROUND_NAME_{LANGUAGE}'][self.type]


class FightRoundEnum(Enum):
    Prepare = 0
    UserRound = 1
    EnemyRound = 2
    Connect = 3
    End = 4


FIGHT_ROUND_NAME_CN = {
    0: '戰鬥前回合',
    1: '我方行動回合',
    2: '敵方行動回合',
    3: '戰鬥後回合',
    4: '戰鬥結算'

}

FIGHT_ROUND_NAME_EN = {
    0: 'BeforeFight',
    1: 'OurRound',
    2: 'EnemyRound',
    3: 'AfterFight',
    4: 'FightEnd'

}