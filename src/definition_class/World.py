import datetime
import time

from definition_class.Stage import CreateHeroStage


class World:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.round_time = 0
        self.players = []
        self.enemy = []
        self.command_text = ''
        self.current_stage = CreateHeroStage()

    def add_round_time(self):
        self.round_time += 1

    def add_date(self):
        self.date += datetime.timedelta(days=1)

    def create(self):
        print('迷宮建立')


test = World()
