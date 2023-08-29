from definition_class import Unit, UnitInfo
from self_package import ObVar
from random import randint

HERO_POINT_RATE = {
    'str': {'hp': 10, 'ad': 2},
    'agi': {'ad': 4, 'sp': 7},
    'int': {'ap': 7, 'sp': 15}
}


class Slime(Unit):
    def __init__(self, hp_limit=100, sp_limit=100, level=1, name='slime'):
        super().__init__(info=UnitInfo(name=name, sp_limit=sp_limit, hp_limit=hp_limit, level=level, race='Slime'))

    def before_die(self):
        pass


class Human(Unit):
    def __init__(self, hp_limit=100, sp_limit=100, name='mage'):
        super().__init__(info=UnitInfo(name=name,
                                       hp_limit=hp_limit,
                                       sp_limit=sp_limit,
                                       race='Human'))

    def before_die(self):
        pass


class Hero(Unit):
    def __init__(self, name, _str: int, _agi: int, _int: int):
        self._str = ObVar(_str, self.observer_points)
        self._agi = ObVar(_agi, self.observer_points)
        self._int = ObVar(_int, self.observer_points)
        self._exp_limit = 100
        self._exp = 0
        default_hp = self._str * HERO_POINT_RATE['str']['hp'] + 100
        default_sp = self._agi * HERO_POINT_RATE['agi']['sp'] + self._int * HERO_POINT_RATE['int']['sp'] + 100
        default_ad = self._str * HERO_POINT_RATE['str']['ad'] + self._agi * HERO_POINT_RATE['agi']['ad'] + 5
        default_ap = self._int * HERO_POINT_RATE['int']['ap']

        super().__init__(info=UnitInfo(name=name,
                                       hp_limit=default_hp,
                                       sp_limit=default_sp,
                                       ad_attack=default_ad,
                                       ap_attack=default_ap,
                                       race='Human'))

    @property
    def exp(self):
        return f'當前經驗條: {self._exp} / {self._exp_limit}'

    def observer_points(self):
        self.hp_limit = self._str * HERO_POINT_RATE['str']['hp'] + 100
        self.sp_limit = self._agi * HERO_POINT_RATE['agi']['sp'] + self._int * HERO_POINT_RATE['int'][
            'sp'] + 100
        self.ad_attack = self._str * HERO_POINT_RATE['str']['ad'] + self._agi * HERO_POINT_RATE['agi']['ad'] + 5
        self.ap_attack = self._int * HERO_POINT_RATE['int']['ap']

    def get_exp(self, exp: int):
        self._exp += exp
        while self._exp >= self._exp_limit:
            self._exp -= self._exp_limit
            self.upgrade()

    def upgrade(self):
        self.level += 1
        print(f'{self.name} 升上等級 {self.level}')
        default_point = 10
        total = self._str.value + self._agi.value + self._int.value
        self._str += round(default_point * (self._str / total))
        self._agi += round(default_point * (self._agi / total))
        self._int += round(default_point * (self._int / total))
        # 生命/魔力全滿
        self.hp = self.hp_limit
        self.sp = self.sp_limit
        # 調整經驗條
        self._exp_limit += (50 + self._exp_limit // 10)

    def before_die(self):
        pass


hero = Hero('ted', 10, 0, 0)
hero.get_exp(10000)
print(hero.show_info())
