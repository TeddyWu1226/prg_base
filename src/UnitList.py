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
