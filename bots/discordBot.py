from discord.ext import commands

from globals import helpers


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(command_prefix=prefix, description=desc)
        self.guild = None
        self.logger = helpers.setup_logger(__name__)

    async def on_ready(self):
        self.guild = helpers.get_guild(self)
        self.logger.info(f'Logged into Discord | {self.guild.name}')






