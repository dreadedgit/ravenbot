from discord.ext import commands
from globals import sqlConfig

class UpdateCog(commands.cog):

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.Cog.listener()
    async def on_



def setup(bot):
    bot.add_cog(UpdateCog(bot))
