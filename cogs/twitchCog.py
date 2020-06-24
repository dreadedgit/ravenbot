from discord.ext import commands

import twitchBot


class TwitchBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitchBot.RaphTwitch()
        self.twitch.loop.create_task(self.twitch.start())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.twitch.modify_webhook_subscription()


def setup(bot):
    bot.add_cog(TwitchBot(bot))
