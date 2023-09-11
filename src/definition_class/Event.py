async def empty_fun():
    pass


class Event:
    def __init__(self, trigger: bool = True, action=empty_fun, working_time=0):
        if not isinstance(trigger, bool):
            raise TypeError('trigger 只能接受布林值')
        if not callable(action):
            raise TypeError('action 只能接受異步FUNCTION')
        if working_time == 0:
            self.undead = True
            self.working_time = 0
        else:
            self.undead = False
            self.working_time = working_time

        self.trigger = trigger
        self.action = action

    async def validate(self, force=False):
        if self.trigger or force:
            return await self.run()
        else:
            return None

    async def run(self):
        if not self.undead:
            if self.working_time <= 0:
                self.destroy()
                return
            else:
                self.working_time = - 1
        await self.action()

    def destroy(self):
        del self
