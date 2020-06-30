from discord.ext import commands

from bots import twitchBot


class TwitchBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitchBot.RaphTwitch()
        self.twitch.load_module('twitchcogs.simpleCommands')
        self.twitch.load_module('twitchcogs.timers')
        self.twitch.loop.create_task(self.twitch.start())


def setup(bot):
    bot.add_cog(TwitchBot(bot))
