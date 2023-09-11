from definition_class.Effect import EffectList

if __name__ == '__main__':
    # hero = Hero(name='ted', _str=10, _agi=10, _int=10)
    # hero.learn(FireBall(level=1))
    # slime1 = Slime(level=1)
    # slime2 = Slime(level=2)
    # test_stage = FightStage([hero], [slime1, slime2])
    from EffectList import EffectPoison, EffectBurn

    test = EffectList(effect_list=[EffectPoison(), EffectPoison(), EffectPoison(), EffectBurn()])
    test._check_is_repeat_effect(EffectBurn())
