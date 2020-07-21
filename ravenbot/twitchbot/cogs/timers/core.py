import asyncio
from random import randint

from twitchio.ext import commands
from ravenbot import Config
from .. import checks

config = Config()
DEFAULT_TIMERS_FILE = {
    "messages": []
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
        if not checks.is_bot(message.author, self.bot):
            # if not checks.is_vip(message.author):
            if not checks.is_mod(message.author):
                if not checks.has_prefix(message):
                    self.count += 1
                    if self.count == 10:
                        await asyncio.sleep(300)
                        await self.timer_message(message)

    # need to figure out sub commands or just use if else like a normie
    # @commands.command(name='timers')
    # async def timers_command(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         pass
    #
    # @commands.command(name='count', cls=timers_command)
    # async def count_command(self, ctx):
    #     print(ctx)


def prep(bot):
    config.load(filename)
    timers = Timers(bot)
    bot.add_cog(timers)
