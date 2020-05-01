from discord.ext import commands
from globals import sqlConfig

class UpdateCog(commands.cog):

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        print('test')



def setup(bot):
    bot.add_cog(UpdateCog(bot))
