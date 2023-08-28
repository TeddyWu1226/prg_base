import abc
from abc import ABC, abstractmethod

from definition_class.Round import Round, FightRoundEnum


class Stage(ABC):
    def __init__(self, default_round: Round, end_round: Round):
        self.default_round = default_round
        self.end_round = end_round
        self.current_round = default_round
        self.is_end = False

    def remake(self):
        self.current_round = self.default_round

    def jump_round(self, to_round: Round):
        self.current_round = to_round

    def next_round(self):
        if self.current_round == self.end_round:
            return
        if self.is_end:
            self.current_round = self.end_round
        else:
            self.regular_round_cycle()

    @abstractmethod
    def regular_round_cycle(self):
        pass

    def set_end_round(self):
        self.is_end = True
        self.next_round()

    @property
    def round_name(self):
        return self.current_round.name

    def __repr__(self):
        return self.current_round

    def __str__(self):
        return str(self.current_round)


class FightStage(Stage):
    def __init__(self):
        super().__init__(default_round=Round(FightRoundEnum.Prepare),
                         end_round=Round(FightRoundEnum.End))

    def regular_round_cycle(self):
        if self.current_round == FightRoundEnum.EnemyRound.value:
            self.current_round = Round(FightRoundEnum.UserRound)
        else:
            self.current_round += 1


test = FightStage()
print(test.round_name)
test.next_round()
print(test.round_name)
test.next_round()
print(test)
test.next_round()
print(test.round_name)
test.next_round()
print(test.round_name)
test.set_end_round()
print(test.round_name)
