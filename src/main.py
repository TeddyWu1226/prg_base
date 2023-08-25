import asyncio
from definition_class import Clock
from SkillList import FireBall, HealingMagic
from UnitList import Slime, Human


async def terminal_command():
    while True:
        command = input('請輸入指令:')
        try:
            print(command)
        except Exception as e:
            print(f'{e}')
        await asyncio.sleep(1)


async def main():
    world_time = Clock()
    tasks = [world_time.run(), terminal_command()]
    await asyncio.gather(*tasks)


# if __name__ == '__main__':
# loop = asyncio.get_event_loop()
#
# try:
#     loop.run_until_complete(main())
# except KeyboardInterrupt:
#     pass
# finally:
#     loop.close()


if __name__ == '__main__':
    print('---角色建立---')
    mage = Human()
    mage.learn(FireBall(damage=100, cost_sp=25))
    slime = Slime(hp_limit=250, level=1)
    slime.learn(HealingMagic(heal=50, cost_sp=20))
    for i in range(0, 6):
        print('---戰鬥回合---')
        mage.FIREBALL(slime)
        slime.HEALING()
