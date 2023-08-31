from dataclasses import dataclass
from definition_class import Unit, UnitInfo


@dataclass
class RaceUpgradeCurve:
    """
    種族成長曲線(每一等成長多少)
    """
    race: str
    hp: int = 0
    sp: int = 0
    ad_attack: int = 0
    ap_attack: int = 0
    ad_df: int = 0
    ap_df: int = 0


class Slime(Unit):
    def __init__(self, level=1, name='slime'):
        grade_curve = RaceUpgradeCurve(
            race='Slime',
            hp=50,
            sp=10,
            ad_attack=5,
            ad_df=0,
            ap_df=2
        )
        super().__init__(info=UnitInfo(name=name,
                                       level=level,
                                       race=grade_curve.race,
                                       hp_limit=50 + level * grade_curve.hp,
                                       sp_limit=100 + level * grade_curve.sp,
                                       ad_attack=10 + level * grade_curve.ad_attack,
                                       ad_df=level * grade_curve.ad_df,
                                       ap_df=level * grade_curve.ap_df
                                       )
                         )

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
