import discord
import settings

from discord.ext import commands


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(command_prefix=prefix, description=desc)

    async def on_ready(self):
        print('logged in to discord')
