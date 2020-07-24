import asyncio
from random import randint

from twitchio.ext import commands
from ravenbot import Config
from .. import checks, utils

config = Config()
DEFAULT_TIMERS_FILE = {
    "messages": {},
    "settings": {
        "time": 300,
        "count": 10
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

    async def event_ready(self):
        self.bot.add_listener(self.message_count, 'event_message')

    async def timer_message(self, message):
        while self.tosend == self.previous:
            x = randint(1, len(self.timers["messages"]))
            x -= 1
            self.tosend = list(self.timers["messages"].values())[x]
        self.count = 0
        self.previous = self.tosend
        await message.channel.send_me(self.tosend)

    async def message_count(self, message):
        if not checks.check_all(message.author, message, self.bot):
            self.count += 1
            if self.count == self.timers["settings"]["count"]:
                await asyncio.sleep(self.timers["settings"]["time"])
                await self.timer_message(message)

    @commands.command(name='timers')
    async def timers_command(self, ctx, *args):
        if not ctx.message.author.is_mod:
            await ctx.send_me(f'{ctx.author.name} only mods are permitted to use this command')
        else:
            if not args or len(args) < 2:
                await ctx.send_me(f'timer trigger set to {self.timers["settings"]["count"]} messages')
                await ctx.send_me(f'timer length set to {self.timers["settings"]["time"]} seconds')
                await ctx.send_me('usage !timers [count|time][int]')
            else:
                if not args[1].isnumeric():
                    await ctx.send_me('usage !timers [count|time][int]')
                else:
                    if args[0] == 'count' or args[0] == 'time':
                        utils.add_item(self.timers, "settings", args[0], int(args[1]), filename)
                        if args[0] == 'count':
                            await ctx.send_me(f'timer trigger set to {self.timers["settings"]["count"]} messages')
                        elif args[0] == 'time':
                            await ctx.send_me(f'timer length set to {self.timers["settings"]["time"]} seconds')
                    else:
                        await ctx.send_me('usage !timers [count|time][int]')

    @commands.command(name='addtimer')
    async def add_timer(self, ctx, *args):
        if not checks.is_mod(ctx.author):
            tosend = f"@{ctx.author.name} only mods can add commands"
        else:
            if len(args) > 0:
                if not utils.contains(self.timers, "messages", args[0]):
                    if len(args) >= 2:
                        response = ' '.join(args[1:])
                        utils.add_item(self.timers, "messages", args[0], str(response), filename)
                        tosend = f"@{ctx.author.name} timer \'{args[0]}\' added"
                    else:
                        tosend = f"@{ctx.author.name} unable to add timer, no message specified"
                else:
                    tosend = f"@{ctx.author.name} timer \'{args[0]}\' already exists"
            else:
                tosend = 'usage !addtimer [identifier] [message]'
        await ctx.send_me(tosend)

    @commands.command(name='deltimer')
    async def delcom(self, ctx, name):
        if not checks.is_mod(ctx.author):
            tosend = f"@{ctx.author.name} only mods can delete timers"
        else:
            if not utils.contains(self.timers, "messages", name):
                tosend = f"@{ctx.author.name} timer \'{name}\' does not exist"
            else:
                utils.delete(self.timers, "messages", name, filename)
                tosend = f"@{ctx.author.name} timer \'{name}\' deleted"
        await ctx.send_me(tosend)


def prep(bot):
    config.load(filename)
    timers = Timers(bot)
    bot.add_cog(timers)
