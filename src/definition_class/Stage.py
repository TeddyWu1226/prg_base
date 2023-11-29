import random
import time
from abc import ABC, abstractmethod
from typing import List
from definition_class.Hero import Hero
from definition_class.Round import Round, FightRoundEnum, CreateHeroRoundEnum, WalkRoundEnum, RestRoundEnum, \
    ConnectRoundEnum
from definition_class.base_class import Unit, TargetType
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

    def select_command(self, hint_text, selection=None, is_animation=False, show_cancel=True):
        """

        :param hint_text:
        :param selection:
        :param is_animation:
        :param show_cancel:
        :return:
        """
        if selection is None:
            selection = ['是', '否']
        if not isinstance(selection, list):
            raise TypeError(f'selection 只能為list ,不能為 {type(selection)} 類型')
        selection_text = ''
        for index, select in enumerate(selection):
            selection_text += f'[{index + 1}] {select}    '
        if show_cancel:
            selection_text += f'[0] 取消'
        is_command_confirm = False
        selected_option = None
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
                if show_cancel and self.command_text == '0':
                    return selected_option
                selected_option = self.check_select_command(selection)
                self.check_command()
                is_command_confirm = True
            except Exception as e:
                print(e)
                pass
        return selected_option

    @property
    def round_name(self):
        return f"~ {self.current_round.name} ~"

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
                enemy_str_list.append(f' 等級{_enemy.level} 的{_enemy.name}')
            print(f'出現了!{",".join(enemy_str_list)}')
            time.sleep(1)
        elif round_value == FightRoundEnum.UserRound.value:
            # 玩家回合前觸發
            self.check_unit_effect(self.players, 'before')
            time.sleep(1)

            # 玩家行動回合
            self.user_action_operate()
            time.sleep(1)

            # 玩家回合後觸發
            self.check_unit_effect(self.players, 'after')
            time.sleep(1)

        elif round_value == FightRoundEnum.EnemyRound.value:
            print('--------')
            print(self.round_name)
            print('')
            time.sleep(1)
            # 敵人回合前觸發
            self.check_unit_effect(self.enemy, 'before')
            time.sleep(1)
            # 敵人行動回合
            self.enemy_action_operate()
            time.sleep(1)

            # 敵人回合後觸發
            self.check_unit_effect(self.enemy, 'after')
            time.sleep(1)

        self.next_round()

    @staticmethod
    def check_unit_effect(uint_group: List[Unit], trigger_time='before'):
        for unit in filter(lambda _unit: not _unit.is_stop and _unit.is_alive, uint_group):
            exec(f'unit.{trigger_time}_round_check_status()')

    def user_action_operate(self):
        print('-----')
        for player in filter(lambda unit: not unit.is_stop, self.players):
            is_active = False
            while not is_active:
                order = self.select_command(hint_text=f'{player.name} 要做什麼?',
                                            selection=['攻擊', '技能', '查看', '查看我方狀態'],
                                            show_cancel=False)
                if order == '攻擊':
                    target = self.select_command(f'選擇哪位目標?', list(filter(lambda unit: unit.is_alive, self.enemy)))
                    if not target:
                        continue
                    print('------')
                    player.attack(target)

                    is_active = True
                elif order == '技能':
                    selected_skill = self.select_command(f'施展哪一個技能?', player.skills)
                    if not selected_skill:
                        continue
                    selected_skill.show_info()
                    if selected_skill.skill_vm.target_type == TargetType.Single.value:
                        target = self.select_command(f'選擇哪位目標?',
                                                     list(filter(lambda unit: unit.is_alive, self.enemy)))
                        if not target:
                            continue
                        exec(f'player.{selected_skill.code}(target)')
                    elif selected_skill.skill_vm.target_type == TargetType.Multiple.value:
                        exec(f'player.{selected_skill.code}(list(filter(lambda unit: unit.is_alive, self.enemy)))')
                    else:
                        exec(f'player.{selected_skill.code}()')
                    is_active = True
                elif order == '查看':
                    target = self.select_command(f'查看哪一位資訊?',
                                                 list(filter(lambda unit: unit.is_alive, self.enemy)))
                    if target:
                        target.show_info()
                    continue
                elif order == '查看我方狀態':
                    target = self.select_command(f'查看哪一位資訊?', self.players)
                    if target:
                        target.show_info()
                self.judge_is_to_end()

    def enemy_action_operate(self):
        for _enemy in filter(lambda unit: not unit.is_stop, self.enemy):
            random_target = random.choice(list(filter(lambda unit: unit.is_alive, self.players)))
            _enemy.attack(random_target)
            self.judge_is_to_end()
            print('')
            time.sleep(1)

    def judge_is_to_end(self):
        if len(list(filter(lambda unit: unit.is_alive, self.players))) == 0:
            print('你輸了!')
            input('輸入任意鍵後關閉')
            exit()
        elif len(list(filter(lambda unit: unit.is_alive, self.enemy))) == 0:
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
            print('')
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
                print('')
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
        self.random_dice = random.randint(1, 4)
        if round_value == WalkRoundEnum.Explore.value:
            for i in range(3, 3 + self.random_dice):
                movie_print('探路中...')

    def check_command(self):
        pass


class RestStage(Stage):
    def __init__(self, players: List[Unit]):
        enum_name = 'REST_ROUND_NAME'
        self.players = players
        super().__init__(default_round=Round(RestRoundEnum.Rest, enum_name),
                         end_round=Round(RestRoundEnum.Rest, enum_name))

    def regular_round_cycle(self):
        pass

    def round_action(self, round_value):
        if round_value == RestRoundEnum.Rest.value:
            print(self.round_name)
            time.sleep(1)
            print(f'我方獲得適當的休息，恢復了1/3的生命與魔力!')
            for player in self.players:
                player.value_percent_change(0.33, 'hp')
                player.value_percent_change(0.33, 'sp')

    def check_command(self):
        pass


class ConnectStage(Stage):
    def __init__(self, players):
        enum_name = 'CONNECT_ROUND_NAME'
        self.players = players
        super().__init__(default_round=Round(ConnectRoundEnum.Connect, enum_name),
                         end_round=Round(ConnectRoundEnum.Connect, enum_name))

    def regular_round_cycle(self):
        pass

    def round_action(self, round_value):
        if round_value == ConnectRoundEnum.Connect.value:
            to_next = False
            while not to_next:
                order = self.select_command('是否前往下一層?', ['查看目前狀態', '前往下一層'], show_cancel=False)
                if order == '查看目前狀態':
                    target = self.select_command(f'查看哪一位資訊?', self.players)
                    if target:
                        target.show_info()
                        if isinstance(target, Hero):
                            print(target.exp)
                            print('-----------')
                elif order == '前往下一層':
                    to_next = True

    def check_command(self):
        pass
