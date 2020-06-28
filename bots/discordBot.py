from discord.ext import commands

from globals import settings


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(command_prefix=prefix, description=desc)
        self.guild = None

    async def on_ready(self):
        self.guild = settings.setguild(self)
        print(f'Logged into Discord | {self.guild.name}')






