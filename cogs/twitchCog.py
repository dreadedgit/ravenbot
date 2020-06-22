from discord.ext import commands as discord_commands
from twitchio.ext import commands as commands

import settings


class RaphTwitch(commands.Bot):

    def __init__(self, bot):
        self.discord_bot = bot
        super().__init__(irc_token=settings.IRC_TOKEN,
                         nick=settings.NICK,
                         prefix=settings.COMMAND_PREFIX,
                         initial_channels=[settings.CHANNEL])

        self.loop.create_task(self.start())


def setup(bot):
    bot.add_cog(RaphTwitch(bot))
