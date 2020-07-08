import asyncio
import sys
import traceback

from twitchio.ext import commands

from settings import helpers

filename = 'cogs/twitch/json/customcommands.json'
data = helpers.open_file(filename)


def is_command(name):
    for c in data["COMMANDS"]:
        if name == c["NAME"]:
            return True


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
        self.cooldown = False

    @commands.command(name='addcom')
    async def add_com(self, ctx, *args):
        if not ctx.author.is_mod:
            r = f'@{ctx.author.name} only mods can add commands'
        else:
            if is_command(args[0]):
                r = f'@{ctx.author.name} command \"{args[0]}\" already exists'
            else:
                full = ' '.join(args[1:])
                addcom(args[0], full)
                r = f'@{ctx.author.name} successfully added command \"{args[0]}\"'
        await ctx.send(r)

    @commands.command(name='delcom')
    async def del_com(self, ctx, name):
        if not ctx.author.is_mod:
            r = f'@{ctx.author.name} only mods can delete commands'
        else:
            if not is_command(name):
                r = f'@{ctx.author.name} command \"{name}\" does not exist'
            else:
                delcom(name)
                r = f'@{ctx.author.name} successfully deleted command \"{name}\"'
        await ctx.send(r)

    async def event_message(self, message):
        if message.author.name != self.bot.nick:
            if message.content.startswith('!'):
                if self.cooldown:
                    await asyncio.sleep(5)
                    self.cooldown = False
                else:
                    if is_command(message.content.strip('!')):
                        await message.channel.send(getresponse(message.content.strip('!')))
                        self.cooldown = True
                    else:
                        await self.bot.handle_commands(message)

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            self.logger.error(f"[{ctx.channel.name}] {error}")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CustomCommands(bot))
