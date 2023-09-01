import os
import time
from enum import Enum


def movie_print(string, speed=0.1):
    for index in range(1, len(string) + 1):
        print(f'\r{string[0:index]}', end='')
        time.sleep(speed)
    print('')


def cmd_clear():
    os.system('cls')


def get_enum_values(enum: Enum):
    return [member.value for member in enum]
