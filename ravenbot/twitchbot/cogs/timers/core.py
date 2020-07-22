import asyncio
from random import randint

from twitchio.ext import commands
from ravenbot import Config
from .. import checks

config = Config()
DEFAULT_TIMERS_FILE = {
    "messages": [],
    "settings": {
        "time": 300,
        "counter": 10
    }
}

filename = 'settings/twitch/timers.yml'


@commands.cog()
class Timers:

    def __init__(self, bot):
        self.bot = bot
        self.timers = config
        if len(self.timers) == 0:
            self.timers.update(DEFAULT_TIMERS_FILE)
            self.timers.write(filename, DEFAULT_TIMERS_FILE)
        self.count = 0
        self.tosend = ''
        self.previous = ''

    def change_setting(self, setting, value):
        self.timers["settings"][setting] = int(value)
        self.timers.write(filename, self.timers)

    async def event_ready(self):
        self.bot.add_listener(self.message_count, 'event_message')

    async def timer_message(self, message):
        while self.tosend == self.previous:
            x = randint(1, len(self.timers["messages"]))
            x -= 1
            self.tosend = self.timers["messages"][x]
        self.count = 0
        self.previous = self.tosend
        await message.channel.send_me(self.tosend)

    async def message_count(self, message):
        if not checks.check_all(message.author, message, self.bot):
            self.count += 1
            if self.count == self.timers["settings"]["counter"]:
                await asyncio.sleep(self.timers["settings"]["time"])
                await self.timer_message(message)

    @commands.command(name='timers')
    async def timers_command(self, ctx, *args):
        if not ctx.message.author.is_mod:
            await ctx.send(f'{ctx.message.author.name} only mods are permitted to use this command')
        else:
            if not args or len(args) < 2:
                await ctx.send(f'timer trigger set to {self.timers["settings"]["counter"]} messages')
                await ctx.send(f'timer length set to {self.timers["settings"]["time"]} seconds')
                await ctx.send(f'usage !timers [count|time][int]')
            else:
                if args[0] == 'count':
                    if not args[1].isnumeric():
                        await ctx.send(f'usage !timers [count|time][int]')
                    else:
                        self.change_setting("counter", args[1])
                        await ctx.send(f'timer trigger set to {self.timers["settings"]["counter"]} messages')
                elif args[0] == 'time':
                    if not args[1].isnumeric():
                        await ctx.send(f'usage !timers [count|time][int]')
                    else:
                        self.change_setting("time", args[1])
                        await ctx.send(f'timer length set to {self.timers["settings"]["time"]} seconds')


def prep(bot):
    config.load(filename)
    timers = Timers(bot)
    bot.add_cog(timers)
