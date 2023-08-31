import datetime
import time
from random import randint

from SkillList import FireBall
from UnitList import Slime
from definition_class.Stage import CreateHeroStage, WalkStage, FightStage, RestStage, ConnectStage


class World:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.round_time = 0
        self.players = []
        self.enemy = []
        self.command_text = ''
        self.current_stage = None
        self.floor = 0

    def add_round_time(self):
        self.round_time += 1

    def add_date(self):
        self.date += datetime.timedelta(days=1)

    def start(self):
        self.current_stage = CreateHeroStage()
        self.players.append(self.current_stage.export_hero())
        time.sleep(2)
        print('※※ 開始冒險 ※※')
        time.sleep(2)
        while True:
            self.dungeon_loop()

    def dungeon_loop(self):
        """
        探路 > 戰鬥 / 休息
        :return:
        """
        self.floor += 1
        print(f'~~~ 第 {self.floor} 層 ~~~')
        self.current_stage = WalkStage()
        dice_value = self.current_stage.random_dice
        if (self.floor % 5 == 1) or dice_value > 2:
            self.create_enemy()
            self.current_stage = FightStage(self.players, self.enemy)
            self.clear_enemy()
        else:
            self.current_stage = RestStage(self.players)
        time.sleep(1)
        self.current_stage = ConnectStage(self.players)
        time.sleep(2)

    def create_enemy(self):
        enemy_level = self.floor // 3
        num = randint(2, 4)
        if self.floor == 1:
            num = 2
        for i in range(1, num):
            _enemy = Slime(level=randint((enemy_level - 1) if enemy_level > 1 else 1, enemy_level + 1),
                           name=f'史萊姆{i}')
            self.enemy.append(_enemy)

    def clear_enemy(self):
        self.enemy = []
