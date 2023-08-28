from definition_class import Unit, UnitInfo


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


HERO_POINT_RATE = {
    'str': {'hp': 20, 'ad': 5},
    'agi': {'ad': 7, 'sp': 15},
    'int': {'ap': 10, 'sp': 30}
}


class Hero(Unit):
    def __init__(self, name, _str: int, _agi: int, _int: int):
        self._str = _str
        self._agi = _agi
        self._int = _int
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

    def before_die(self):
        pass
