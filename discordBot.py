import settings

from discord.ext import commands


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(command_prefix=prefix, description=desc)
        self.guild = None

    async def on_ready(self):
        self.guild = settings.setGuild(self)
        print(f'Logged into Discord | {self.guild.name}')






