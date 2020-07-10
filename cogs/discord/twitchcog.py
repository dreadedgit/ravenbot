import asyncio
from random import randint

from discord.ext import commands as commands
from twitchio.ext import commands as tcommands

from bots import twitchbot
from settings.helpers import write_file, open_file, get_twitch, get_channel, get_role


# FOLLOWAGE RELATED
def format_date(s):
    date = '-'.split(s)
    year = date[0]
    month = date[1]
    day = date[2]
    formatted = f'{month}/{day}/{year}'
    return formatted


async def getfollow(ctx, user_data):
    if len(user_data) == 1:
        tosend = f'@{ctx.author.name} you cannot follow yourself'
    elif len(user_data) == 2:
        follow = await twitch.get_follow(user_data[0].id, user_data[1].id)
        date = format_date(follow["followed_at"].split("T")[0])
        tosend = f'@{ctx.author.name}: {ctx.author.name} has been following {ctx.channel.name} since {date}'
    else:
        print('error')
        tosend = f'@{ctx.author.name} an unexpected error occurred'
    await ctx.send(tosend)


@tcommands.command(name="followage")
async def followage(ctx):
    user_data = await twitch.get_users(ctx.author.name, ctx.channel.name)
    await getfollow(ctx, user_data)


# CUSTOM TWITCH COMMANDS
commandsfile = 'settings/json/customcommands.json'
coms = open_file(commandsfile)


def is_command(name):
    for c in coms["COMMANDS"]:
        if name == c["NAME"]:
            return True


def del_com(name):
    for c in coms["COMMANDS"]:
        if name == c["NAME"]:
            coms["COMMANDS"].remove(c)
            break
    write_file(coms, commandsfile)


def add_com(name, full):
    c = {
        "NAME": name,
        "REPLY": full
    }
    coms["COMMANDS"].append(c)
    write_file(coms, commandsfile)


def getresponse(name):
    r = ''
    for c in coms["COMMANDS"]:
        if name == c["NAME"]:
            r = c["REPLY"]
            break
    return r


@tcommands.command(name='delcom')
async def delcom(ctx, name):
    if not ctx.author.is_mod:
        r = f'@{ctx.author.name} only mods can delete commands'
    else:
        if not is_command(name):
            r = f'@{ctx.author.name} command \"{name}\" does not exist'
        else:
            del_com(name)
            r = f'@{ctx.author.name} successfully deleted command \"{name}\"'
    await ctx.send(r)


@tcommands.command(name='addcom')
async def addcom(ctx, *args):
    if not ctx.author.is_mod:
        r = f'@{ctx.author.name} only mods can add commands'
    else:
        if is_command(args[0]):
            r = f'@{ctx.author.name} command \"{args[0]}\" already exists'
        else:
            full = ' '.join(args[1:])
            add_com(args[0], full)
            r = f'@{ctx.author.name} successfully added command \"{args[0]}\"'
    await ctx.send(r)


# TIMER RELATED
timersfile = 'settings/json/timers.json'
timers = open_file(timersfile)


async def timer_message(message):
    while twitch.tosend == twitch.previous:
        x = randint(1, len(timers["MESSAGES"]))
        x -= 1
        twitch.tosend = timers["MESSAGES"][x]
    twitch.count = 0
    await message.channel.send_me(twitch.tosend)


# TWITCH BOT SETUP
def is_cooldown():
    return twitch.cooldown


TWITCH_CHANNEL = get_twitch("CHANNELS")[0]
twitch = twitchbot.RavenbotT()
twitch.add_command(followage)
twitch.add_command(addcom)
twitch.add_command(delcom)

# DISCORD INTEGRATION

livefile = 'cogs/discord/json/livenotif.json'
live = open_file(livefile)
CHANNEL_NAME = live["CHANNEL"]["NAME"]
ROLE_ID = live["ROLE"]["ID"]


class RavenbotTCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.role = None

    async def twitch_message(self, message):
        if message.author.name != twitch.nick:
            if message.content.startswith('!'):
                if is_cooldown:
                    await asyncio.sleep(3)
                    twitch.cooldown = False
                else:
                    if is_command(message.content.strip('!')):
                        await message.channel.send(getresponse(message.content.strip('!')))
                        twitch.cooldown = True
            else:
                twitch.count += 1
                twitch.logger.log(5, f'{message.author.name}: {message.content}')
                if twitch.count == 10:
                    await asyncio.sleep(60)
                    await timer_message(message)
                    twitch.previous = twitch.tosend

    @commands.Cog.listener()
    async def on_ready(self):
        twitch.add_listener(self.twitch_message, "event_message")
        await twitch.start()
        self.channel = get_channel(self.bot, CHANNEL_NAME)
        self.role = get_role(self.bot, ROLE_ID)
        await self.check_if_live()

    async def check_if_live(self):
        is_live = False
        while True:
            stream = await twitch.get_stream(TWITCH_CHANNEL)
            if is_live:
                if stream is not None:
                    is_live = True
                else:
                    is_live = False
            else:
                if stream is not None:
                    await self.send_live_message(stream)
                    is_live = True
                else:
                    is_live = False
            await asyncio.sleep(120)

    async def send_live_message(self, stream):
        link = f'https://www.twitch.tv/{stream["user_name"]}'
        await self.channel.send(f'{self.role.mention} {link}')


def setup(bot):
    bot.add_cog(RavenbotTCog(bot))