import asyncio
from random import randint

from twitchio.ext import commands

from settings import helpers

filename = 'cogs/twitch/json/timers.json'
data = helpers.open_file(filename)


@commands.cog()
class TimerCog:

    def __init__(self, bot):
        self.tosend = ''
        self.previous = ''
        self.bot = bot
        self.m = 0

    async def timer_message(self, message):
        while self.tosend == self.previous:
            x = randint(1, len(data["MESSAGES"]))
            x -= 1
            self.tosend = data["MESSAGES"][x]
        self.m = 0
        await message.channel.send(self.tosend)

    async def event_message(self, message):
        if not message.author.name == self.bot.nick:
            if not message.content.startswith('!'):
                self.m += 1
                if self.m == 10:
                    await asyncio.sleep(60)
                    await self.timer_message(message)
                    self.previous = self.tosend
            else:
                pass
