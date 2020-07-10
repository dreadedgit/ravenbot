from discord.ext import commands

from settings.helpers import get_discord, get_guild
from utility import logger as logging


class Ravenbot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=get_discord("COMMAND PREFIX"),
            description=get_discord("DESCRIPTION")
        )
        self.guild = None
        self.logger = None

    async def on_ready(self):
        self.guild = get_guild(self)
        self.logger = logging.get_logger(__name__)
        logging.setup_logger(self.logger)
        self.logger.info(f'Logged into Discord | {self.guild.name}')
