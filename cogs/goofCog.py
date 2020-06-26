from discord.ext import commands

import settings


class GoofCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.memesChannel = None


def setup(bot):
    bot.add_cog(GoofCog(bot))

