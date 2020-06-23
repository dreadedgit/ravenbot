from discord.ext import commands

import twitchBot


class TwitchBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        twitch = twitchBot.RaphTwitch()
        twitch.loop.create_task(twitch.start())


def setup(bot):
    bot.add_cog(TwitchBot(bot))
