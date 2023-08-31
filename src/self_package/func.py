import os
import time


def movie_print(string, speed=0.1):
    for index in range(1, len(string) + 1):
        print(f'\r{string[0:index]}', end='')
        time.sleep(speed)


def cmd_clear():
    os.system('cls')
