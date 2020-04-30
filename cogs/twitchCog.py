from discord.ext import commands
from globals import twitch

class TwitchCog(commands.Cog):

    def __init__(self, bot):
        twitch.run()

        self.discord_bot = bot

def setup(bot):
    bot.add_cog(TwitchCog(bot))
