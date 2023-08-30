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
        self.current_stage = None

    def add_round_time(self):
        self.round_time += 1

    def add_date(self):
        self.date += datetime.timedelta(days=1)

    def start(self):
        self.current_stage = CreateHeroStage()
        self.players.append(self.current_stage.export_hero())
        print(self.players)

    def dungeon_loop(self):
        """
        探路 > 戰鬥 / 休息
        :return:
        """
        pass


# world = World()
# world.start()
