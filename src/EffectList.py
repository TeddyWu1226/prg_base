from definition_class import EffectStatus


class EffectDizzy(EffectStatus):

    def __init__(self, duration=0.0, is_permanent=False):
        super().__init__('Dizzy', duration, is_permanent)

    def get_effect_text(self) -> str:
        return '不能採取任何動作'

    def get_effect(self) -> dict:
        return {'style': 'negative'}

    def before_destroy(self):
        pass
