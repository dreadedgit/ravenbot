import asyncio
import sys
import traceback

from twitchio.ext import commands

from settings import helpers

filename = 'cogs/twitch/json/customcommands.json'
data = helpers.open_file(filename)


def is_command(name):
    result = False
    for c in data["COMMANDS"]:
        if name == c["NAME"]:
            result = True
            break
    return result


def delcom(name):
    for c in data["COMMANDS"]:
        if name == c["NAME"]:
            data["COMMANDS"].remove(c)
            break
    helpers.write_file(data, filename)


def addcom(name, full):
    c = {
        "NAME": name,
        "REPLY": full
    }
    data["COMMANDS"].append(c)
    helpers.write_file(data, filename)


def getresponse(name):
    r = ''
    for c in data["COMMANDS"]:
        if name == c["NAME"]:
            r = c["REPLY"]
            break
    return r


@commands.cog()
class CustomCommands:

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = 0
        self.logger = helpers.setup_logger(__name__)

    @commands.command(name='addcom')
    async def _add_com(self, ctx, name, *response):
        if not ctx.author.is_mod:
            r = f'@{ctx.author.name} only mods can add commands'
        else:
            if is_command(name):
                r = f'@{ctx.author.name} command \"{name}\" already exists'
            else:
                full = ' '.join(response)
                addcom(name, full)
                r = f'@{ctx.author.name} successfully added command \"{name}\"'
        await ctx.send(content=r)

    @commands.command(name='delcom')
    async def _del_com(self, ctx, name):
        if not ctx.author.is_mod:
            r = f'@{ctx.author.name} only mods can delete commands'
        else:
            if not is_command(name):
                r = f'@{ctx.author.name} command \"{name}\" does not exist'
            else:
                delcom(name)
                r = f'@{ctx.author.name} successfully deleted command \"{name}\"'
        await ctx.send(content=r)

    async def event_message(self, message):
        if not message.author.name == self.bot.nick:
            if message.content.startswith('!'):
                if self.cooldown == 1:
                    await asyncio.sleep(5)
                    self.cooldown = 0
                elif is_command(message.content.strip('!')) & self.cooldown == 0:
                    await message.channel.send(content=getresponse(message.content.strip('!')))
                    self.cooldown = 1
                else:
                    await self.bot.handle_commands(message)

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            self.logger.error(f"[{ctx.channel.name}] {error}")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
