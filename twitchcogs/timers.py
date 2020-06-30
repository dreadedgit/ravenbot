import json
from random import randint
import asyncio

from twitchio.ext import commands


@commands.cog(name='timers')
class TimerCog:

    def __init__(self, bot):
        self.tosend = ''
        self.previous = ''
        self.bot = bot
        self.m = 0

        with open('json/timermessages.json') as json_file:
            self.data = json.load(json_file)
        json_file.close()

    async def timer_message(self, message):
        while self.tosend == self.previous:
            x = randint(1, len(self.data["messages"]))
            x -= 1
            self.tosend = self.data["messages"][x]
        self.m = 0
        await message.channel.send(self.tosend)

    async def event_message(self, message):
        if not message.author.name == self.bot.nick:
            if not message.content.startswith('!'):
                self.m += 1
                if self.m == 10:
                    await asyncio.sleep(30)
                    await self.timer_message(message)
                    self.previous = self.tosend
            else:
                pass
