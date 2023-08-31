import collections
import random
from dataclasses import dataclass, field
from enum import Enum

from colorama import init

init(autoreset=True)


class PartEnum(Enum):
    Head = 'Head'
    Chest = 'Chest'
    Legs = 'Legs'
    Accessory = 'Accessory'
    Ring = 'Ring'
    Cloak = 'Cloak'
    LeftHand = 'LeftHand'  # 副手
    RightHand = 'RightHand'  # 主武器


PART_NAME_CN = {
    'Head': '頭部',
    'Chest': '身體',
    'Legs': '腳部',
    'Accessory': '飾品',
    'Ring': '戒指',
    'Cloak': '披風',
    'LeftHand': '副手',
    'RightHand': '主武器'
}


class QualityEnum(Enum):
    Deity = 8
    Demonise = 7
    Legend = 6
    Perfect = 4
    Excellent = 3
    Good = 2
    Normal = 1
    Old = 0


QUALITY_NAME_CN = {
    0: '破舊',
    1: '普通',
    2: '\033[34m不錯',
    3: '\033[32m精良',
    4: '\033[35m完美',
    6: '\033[36m傳說',
    7: '\033[31m魔',
    8: '\033[33m神'
}


@dataclass
class Equipment:
    part: PartEnum
    name: str
    quality: QualityEnum = None
    description: str = ''
    ad: int = 0
    ap: int = 0
    ad_df: int = 0
    ap_df: int = 0
    hp: int = 0
    sp: int = 0
    crit_rate: float = 0
    dodge_rate: float = 0
    equip_value: float = 0

    def set_equip_value(self):
        if self.quality is None:
            special_add = 0
            self.equip_value = (self.ad + self.ap) * 10 + (self.hp + self.sp) // 10 + self.ad_df + self.ap_df + (
                    self.crit_rate + self.dodge_rate) * 1000
            if self.crit_rate > 0.35:
                special_add += 500
            elif self.crit_rate > 0.25:
                special_add += 250
            if self.dodge_rate > 0.6:
                special_add += 1000
            elif self.dodge_rate > 0.4:
                special_add += 500
            self.equip_value += special_add
            if self.equip_value >= 1000:
                self.quality = QualityEnum.Perfect
            elif self.equip_value >= 800:
                self.quality = QualityEnum.Excellent
            elif self.equip_value >= 500:
                self.quality = QualityEnum.Good
            elif self.equip_value >= 100:
                self.quality = QualityEnum.Normal
            else:
                self.quality = QualityEnum.Old

    def show(self):
        if not self.equip_value:
            self.set_equip_value()
        des_name = f'{QUALITY_NAME_CN[self.quality.value]}的{self.name}\033[0m'
        print('----裝備敘述----')
        print(f'名稱: {des_name}')
        print(f'部位: {PART_NAME_CN[self.part.value]}')
        print(f'敘述: {self.description}')
        print(f'數值: {self.equip_value}')
        if self.ad:
            print(f'攻擊力: +{self.ad}')
        if self.ap:
            print(f'魔力: +{self.ap}')
        if self.hp:
            print(f'生命: +{self.hp}')
        if self.sp:
            print(f'法力: +{self.sp}')
        if self.ad_df:
            print(f'物理防禦: +{self.ad_df}')
        if self.ap_df:
            print(f'魔法防禦: +{self.ap_df}')
        if self.crit_rate:
            print(f'爆擊率: +{round(self.crit_rate * 100)}%')
        if self.dodge_rate:
            print(f'閃避率: +{round(self.dodge_rate * 100)}%')
        print('---------------')


class EquipError:
    @property
    def AlreadyHave(self):
        return 'AlreadyHave'

    @property
    def NotAllow(self):
        return 'NotAllow'


class EquipFlied:
    def __init__(self, disable: list = None):
        if disable is None:
            disable = []
        self.flied = {}
        for part in PartEnum:
            if part.value in disable:
                continue
            self.flied[part.value] = None

    def equip(self, equipment: Equipment):
        if equipment.part.value not in self.flied.keys():
            return EquipError.NotAllow
        elif self.flied[equipment.part.value] is not None:
            return EquipError.AlreadyHave
        self.flied[equipment.part.value] = equipment


def create_random_equip():
    part = PartEnum(random.choice(list(PART_NAME_CN.keys())))
    limit = {
        'ad': 0,
        'ap': 0,
        'hp': 0,
        'sp': 0,
        'ad_df': 0,
        'ap_df': 0,
        'crit_rate': 0,
        'dodge_rate': 0
    }
    equip_name = None
    if part == PartEnum.RightHand:
        weapon_names = ["劍", "匕首", "錘", "長劍", "弓", "武士刀", "魔杖", "巨劍", "戰爪", "斧頭"]
        equip_name = random.choice(weapon_names)

        limit['ad'] = random.randint(10, 100)
        limit['ap'] = random.randint(10, 200)
        limit['crit_rate'] = random.uniform(0.0, 0.8)
    elif part == PartEnum.LeftHand:
        offhand_equipment = ["盾牌", "匕首", "法杖", "箭袋", "法符", "蓄能球", "魔法書"]
        equip_name = random.choice(offhand_equipment)

        limit['ad'] = random.randint(0, 50)
        limit['ap'] = random.randint(0, 100)
        limit['hp'] = random.randint(0, 300)
        limit['sp'] = random.randint(0, 600)
        if equip_name == '盾牌':
            limit['ad_df'] = random.randint(10, 100)
            limit['ap_df'] = random.randint(10, 100)
    elif part == PartEnum.Head:
        heads = ['頭盔', '法帽', '皮帽', '兜帽']
        equip_name = random.choice(heads)

        limit['hp'] = random.randint(0, 1000)
        limit['sp'] = random.randint(0, 1000)
        limit['ad_df'] = random.randint(0, 50)
        limit['ap_df'] = random.randint(0, 50)

    elif part == PartEnum.Chest:
        chests = ['皮甲', '鐵甲', '法袍', '骨甲', '布衣', '鎖子甲']
        equip_name = random.choice(chests)

        limit['hp'] = random.randint(0, 3000)
        limit['sp'] = random.randint(0, 1000)
        limit['ad_df'] = random.randint(0, 200)
        limit['ap_df'] = random.randint(0, 200)

    elif part == PartEnum.Legs:
        legs_name = ['鐵製護腿', '皮褲', '布褲', '鎖子護腿', '袍褲', '骨製護腿']
        equip_name = random.choice(legs_name)

        limit['hp'] = random.randint(0, 1000)
        limit['sp'] = random.randint(0, 200)
        limit['ad_df'] = random.randint(0, 80)
        limit['ap_df'] = random.randint(0, 80)
        limit['dodge_rate'] = random.uniform(0.0, 0.3)

    elif part == PartEnum.Accessory:
        accessory_list = ['項鍊', '墜飾', '徽章', '吊飾']
        equip_name = random.choice(accessory_list)

        limit['hp'] = random.randint(0, 500)
        limit['sp'] = random.randint(0, 1000)
        limit['dodge_rate'] = random.uniform(0.0, 0.2)
    elif part == PartEnum.Ring:
        equip_name = '戒指'

        limit['ad'] = random.randint(0, 50)
        limit['ap'] = random.randint(0, 50)
        limit['hp'] = random.randint(0, 1000)
        limit['sp'] = random.randint(0, 1000)
        limit['crit_rate'] = random.uniform(0.0, 0.4)
        limit['dodge_rate'] = random.uniform(0.0, 0.2)
    elif part == PartEnum.Cloak:
        cloaks = ['披風', '天使之翼', '惡魔之翼', '大衣']
        equip_name = random.choice(cloaks)

        limit['hp'] = random.randint(0, 1500)
        limit['sp'] = random.randint(0, 1500)
        limit['dodge_rate'] = random.uniform(0.2, 0.6)

    ad = random.randint(0, limit.get('ad'))
    ap = random.randint(0, limit.get('ap'))
    hp = random.randint(0, limit.get('hp'))
    sp = random.randint(0, limit.get('sp'))
    ad_df = random.randint(0, limit.get('ad_df'))
    ap_df = random.randint(0, limit.get('ap_df'))
    crit_rate = round(random.uniform(0, limit.get('crit_rate')), 2)
    dodge_rate = round(random.uniform(0, limit.get('dodge_rate')), 2)

    random_equip = Equipment(part=part,
                             name=equip_name,
                             ad=ad,
                             ap=ap,
                             hp=hp,
                             sp=sp,
                             ad_df=ad_df,
                             ap_df=ap_df,
                             crit_rate=crit_rate,
                             dodge_rate=dodge_rate
                             )

    # random_equip.show()
    random_equip.set_equip_value()
    return random_equip


items = []
for i in range(0, 1000):
    item = create_random_equip()
    item.show()
    items.append(item.quality)

c = collections.Counter(items)
print(c)
