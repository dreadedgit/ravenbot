import asyncio

from twitchio.ext import commands
from ravenbot import Config
from .. import checks, utils

config = Config()
DEFAULT_COMMANDS_FILE = {
    "commands": {}
}

filename = 'settings/twitch/commands.yml'


@commands.cog()
class CustomCommands:

    def __init__(self, bot):
        self.bot = bot
        self.customcoms = config
        self.cooldown = False
        if len(self.customcoms) == 0:
            self.customcoms.update(DEFAULT_COMMANDS_FILE)
            self.customcoms.write(filename, DEFAULT_COMMANDS_FILE)

    def get_response(self, name):
        if utils.contains(self.customcoms, "commands", name):
            return self.customcoms["commands"].get(name)

    async def event_ready(self):
        self.bot.add_listener(self.handle_custom_commands, 'event_message')

    async def handle_custom_commands(self, message):
        if not checks.is_bot(message.author, self.bot):
            if checks.has_prefix(message):
                if self.cooldown:
                    await asyncio.sleep(3)
                    self.cooldown = False
                else:
                    if utils.contains(self.customcoms, "commands", message.content.strip('!')):
                        await message.channel.send(self.get_response(message.content.strip('!')))
                        self.cooldown = True

    @commands.command()
    async def addcom(self, ctx, *args):
        if not checks.is_mod(ctx.author):
            tosend = f"@{ctx.author.name} only mods can add commands"
        else:
            if len(args) >= 2:
                if not utils.contains(self.customcoms, "commands", args[0]):
                    response = ' '.join(args[1:])
                    utils.add_item(self.customcoms, "commands", args[0], response, filename)
                    tosend = f"@{ctx.author.name} command \'{args[0]}\' added"
                else:
                    tosend = f"@{ctx.author.name} command \'{args[0]}\' already exists"
            else:
                tosend = f"@{ctx.author.name} unable to add command, no response specified"
        await ctx.send(tosend)

    @commands.command()
    async def delcom(self, ctx, name):
        if not checks.is_mod(ctx.author):
            tosend = f"@{ctx.author.name} only mods can delete commands"
        else:
            if not utils.contains(self.customcoms, "commands", name):
                tosend = f"@{ctx.author.name} command \'{name}\' does not exist"
            else:
                utils.delete(self.customcoms, "commands", name, filename)
                tosend = f"@{ctx.author.name} command \'{name}\' deleted"
        await ctx.send(tosend)


def prep(bot):
    config.load(filename)
    custom = CustomCommands(bot)
    bot.add_cog(custom)
