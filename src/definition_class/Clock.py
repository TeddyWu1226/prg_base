import asyncio
import datetime


class Clock:
    def __init__(self):
        self.time = datetime.datetime.now()
        print(f'開始運行:{self.time}')

    async def run(self):
        while True:
            self.time = datetime.datetime.now()
            await asyncio.sleep(1)  # 等待1秒钟

    def getTime(self):
        print(self.time)

