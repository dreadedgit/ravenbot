from discord.ext import commands

from settings import helpers


class Ravenbot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=helpers.get_discord("COMMAND PREFIX"),
            description=helpers.get_discord("DESCRIPTION")
        )
        self.guild = None
        self.logger = helpers.setup_logger(__name__)

    async def on_ready(self):
        self.guild = helpers.get_guild(self)
        self.logger.info(f'Logged into Discord | {self.guild.name}')
