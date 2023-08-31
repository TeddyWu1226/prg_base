import time

from definition_class import World
from self_package.func import movie_print

if __name__ == '__main__':
    movie_print('---------------------', 0.01)
    movie_print('｜　　無　盡　地　宮　　｜')
    movie_print('---------------------', 0.01)
    time.sleep(1)
    input('輸入任意字開始遊戲:')
    movie_print('準備中...')
    world = World()
    world.start()
