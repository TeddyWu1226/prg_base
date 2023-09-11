from definition_class.Effect import EffectStatus


class EffectBurn(EffectStatus):
    def at_round_before(self):
        pass

    def at_round_after(self):
        pass

    def trigger(self):
        pass

    def __init__(self, duration=2, is_permanent=False):
        super().__init__('燃燒', duration, is_permanent)


class EffectPoison(EffectStatus):
    def __init__(self, damage=10, duration=2):
        self.damage = damage
        super().__init__('中毒', duration)

    def at_round_before(self):
        pass

    def at_round_after(self):
        self.trigger()

    def trigger(self):
        self.owner.attacked(self.giver, self.damage, 'dir')
        print(f'{self.owner} 毒傷發作')
