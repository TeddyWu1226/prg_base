import datetime


class World:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.round_time = 0
        self.players = []
        self.enemy = []

    def add_round_time(self):
        self.round_time += 1

    def add_date(self):
        self.date += datetime.timedelta(days=1)


test = World()
