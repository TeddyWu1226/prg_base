import random
import time
from abc import ABC, abstractmethod
from typing import List

from UnitList import Hero
from definition_class import Unit
from definition_class.Round import Round, FightRoundEnum, CreateHeroRoundEnum, WalkRoundEnum, RestRoundEnum
from self_package.func import movie_print


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
            print('----------')
            print('戰鬥結束!')
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

    def check_select_command(self, selection):
        select_num = int(self.command_text) - 1
        if select_num >= len(selection):
            raise
        return selection[select_num]

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

    def select_command(self, hint_text, selection=None, is_animation=False):
        if selection is None:
            selection = ['是', '否']
        if not isinstance(selection, list):
            raise TypeError(f'selection 只能為list ,不能為 {type(selection)} 類型')
        selection_text = ''
        for index, select in enumerate(selection):
            selection_text += f'[{index + 1}] {select}    '
        is_command_confirm = False
        ans = None
        while not is_command_confirm:
            try:
                if is_animation:
                    movie_print(hint_text)
                    movie_print(selection_text)
                else:
                    print(hint_text)
                    print(selection_text)
                self.command_text = input(f'你的選擇(輸入編號):')
                time.sleep(0.1)
                self.command_text = self.check_select_command(selection)
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

    def __init__(self, players, enemy):
        self.players = players
        self.enemy = enemy
        enum_name = 'FIGHT_ROUND_NAME'
        super().__init__(default_round=Round(FightRoundEnum.Prepare, enum_name),
                         end_round=Round(FightRoundEnum.End, enum_name))

    def round_action(self, round_value):
        if round_value == FightRoundEnum.Prepare.value:
            enemy_str_list = []
            for _enemy in self.enemy:
                enemy_str_list.append(f'等級{_enemy.level}的{_enemy.name}')
            print(f'出現了 {",".join(enemy_str_list)}')
            time.sleep(1)
        elif round_value == FightRoundEnum.UserRound.value:
            self.user_action_operate()
        elif round_value == FightRoundEnum.EnemyRound.value:
            pass
        self.next_round()

    def user_action_operate(self):
        print('-----')
        for player in self.players:
            order = self.select_command(f'{player.name} 要做什麼?', ['攻擊', '技能', '防禦', '逃跑'])
            if order == '攻擊':
                target = self.select_command(f'選擇哪位目標?', list(filter(lambda unit: unit.is_alive, self.enemy)))
                player._attack(target)
            if len(list(filter(lambda unit: unit.is_alive, self.enemy))) == 0:
                self.set_end_round()

    def regular_round_cycle(self):
        if self.current_round == FightRoundEnum.EnemyRound.value:
            self.current_round = Round(FightRoundEnum.UserRound, 'FIGHT_ROUND_NAME')
        else:
            self.current_round += 1
        self.round_action(self.current_round)

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
        self.random_dice = 0
        enum_name = 'WALK_ROUND_NAME'
        super().__init__(default_round=Round(WalkRoundEnum.Explore, enum_name),
                         end_round=Round(WalkRoundEnum.Explore, enum_name))

    def regular_round_cycle(self):
        pass

    def round_action(self, round_value):
        self.random_dice = random.randint(1, 6)
        if round_value == WalkRoundEnum.Explore.value:
            for i in range(3, 3 + self.random_dice):
                movie_print('探路中...')

    def check_command(self):
        pass


class RestStage(Stage):
    def __init__(self, players: List[Unit]):
        enum_name = 'REST_ROUND_NAME'
        super().__init__(default_round=Round(RestRoundEnum.Rest, enum_name),
                         end_round=Round(RestRoundEnum.Rest, enum_name))
        self.players = players

    def regular_round_cycle(self):
        pass

    def round_action(self, round_value):
        if round_value == RestRoundEnum.Rest.value:
            for player in self.players:
                player.value_percent_change(0.33, 'hp')
                player.value_percent_change(0.33, 'sp')

    def check_command(self):
        pass
