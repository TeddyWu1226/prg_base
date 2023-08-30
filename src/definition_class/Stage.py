import random
import time
from abc import ABC, abstractmethod

from UnitList import Hero
from definition_class import Unit
from definition_class.Round import Round, FightRoundEnum, CreateHeroRoundEnum, WalkRoundEnum


class Stage(ABC):
    def __init__(self, default_round: Round, end_round: Round):
        self.default_round = default_round
        self.end_round = end_round
        self.current_round = default_round
        self.command_text = ''
        self.is_end = False
        self.round_action(self.default_round)

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

    def set_end_round(self):
        self.is_end = True
        self.next_round()

    @abstractmethod
    def regular_round_cycle(self):
        pass

    @abstractmethod
    def round_action(self, round_value):
        pass

    @abstractmethod
    def check_command(self):
        pass

    def command(self, hint_text):
        is_command_confirm = False
        while not is_command_confirm:
            try:
                self.command_text = input(f'{hint_text}:')
                time.sleep(0.1)
                self.check_command()
                is_command_confirm = True
            except Exception as e:
                print(e)
                pass
        return self.command_text

    @property
    def round_name(self):
        return self.current_round.name

    def __repr__(self):
        return self.current_round

    def __str__(self):
        return str(self.current_round)


class FightStage(Stage):

    def __init__(self):
        enum_name = 'FIGHT_ROUND_NAME'
        super().__init__(default_round=Round(FightRoundEnum.Prepare, enum_name),
                         end_round=Round(FightRoundEnum.End, enum_name))

    def round_action(self, round_value):
        if round_value == FightRoundEnum.Prepare.value:
            self.command('')

    def regular_round_cycle(self):
        if self.current_round == FightRoundEnum.EnemyRound.value:
            self.current_round = Round(FightRoundEnum.UserRound, 'FIGHT_ROUND_NAME')
        else:
            self.current_round += 1

    def check_command(self):
        pass


class CreateHeroStage(Stage):
    def __init__(self):
        self.user_hero = None
        enum_name = 'CREATE_HERO_ROUND_NAME'
        super().__init__(default_round=Round(CreateHeroRoundEnum.Create, enum_name),
                         end_round=Round(CreateHeroRoundEnum.Create, enum_name))

    def round_action(self, round_value):
        if round_value == CreateHeroRoundEnum.Create.value:
            print(self.round_name)
            self.user_hero = self.create_hero()

    def create_hero(self) -> Unit:
        hero_name = self.command('請輸入角色名稱')

        is_check = False
        current_hero = None
        while not is_check:
            try:
                default_point = 10
                print(f'---設置初始屬性,共有{default_point}點---')
                hero_str = int(self.command(f'請分配點數給力量(目前有{default_point})'))
                default_point -= hero_str
                if default_point < 0:
                    print('點數不足，請重新配置')
                    continue
                hero_agi = int(self.command(f'請分配點數給敏捷(目前有{default_point})'))
                default_point -= hero_agi
                if default_point < 0:
                    print('點數不足，請重新配置')
                    continue
                hero_int = int(self.command(f'請分配點數給智力(目前有{default_point})'))
                default_point -= hero_int
                if default_point < 0:
                    print('點數不足，請重新配置')
                    continue
                current_hero = Hero(name=hero_name, _str=hero_str, _agi=hero_agi, _int=hero_int)
                print('您即將創造')
                print('-------------')
                print(f'名稱:{current_hero.name}')
                print(f'HP:{current_hero.hp}')
                print(f'SP:{current_hero.sp}')
                print(f'攻擊力:{current_hero.ad_attack}')
                print(f'魔力:{current_hero.ap_attack}')
                print('-------------')
                check_text = input('您確定嗎?(確認請輸入Y,輸入其他內容將重新配點):')
                is_check = check_text == 'Y'
            except ValueError:
                print('請輸入阿拉伯數字，將重新配點')
                print('-------------')
                continue
        return current_hero

    def regular_round_cycle(self):
        pass

    def export_hero(self):
        return self.user_hero

    def check_command(self):
        pass


class WalkStage(Stage):
    def __init__(self):
        enum_name = 'WALK_ROUND_NAME'
        super().__init__(default_round=Round(WalkRoundEnum.Explore, enum_name),
                         end_round=Round(WalkRoundEnum.Explore, enum_name))

    def regular_round_cycle(self):
        pass

    def round_action(self, round_value):
        def movie_print(string, speed=0.1):
            for index in range(1, len(string) + 1):
                print(f'\r{string[0:index]}', end='')
                time.sleep(speed)

        if round_value == WalkRoundEnum.Explore.value:
            random_int = random.randint(4, 9)
            for i in range(0, random_int):
                movie_print('探路中...')

    def check_command(self):
        pass


test = WalkStage()
