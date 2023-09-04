from definition_class import EffectStatus


class EffectBurn(EffectStatus):
    def at_round_before(self):
        pass

    def at_round_after(self):
        pass

    def trigger(self):
        pass

    def __init__(self, duration=2, is_permanent=False):
        super().__init__('燃燒', duration, is_permanent)
