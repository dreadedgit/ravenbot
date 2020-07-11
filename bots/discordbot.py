from discord.ext import commands

from settings.helpers import get_discord, get_guild


class Ravenbot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=get_discord("COMMAND PREFIX"),
            description=get_discord("DESCRIPTION")
        )
        self.guild = None

    async def on_ready(self):
        self.guild = get_guild(self)
        print(f'[INFO]Logged into Discord | {self.guild.name}')
