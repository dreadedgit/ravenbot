import asyncio

from discord.ext import commands
from bots import twitchBot
from globals.settings import CHANNEL, LIVE_CHANNEL
from globals import helpers


class TwitchBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitchBot.RaphTwitch()
        self.twitch.load_module('twitchcogs.simpleCommands')
        self.twitch.load_module('twitchcogs.timers')
        self.twitch.loop.create_task(self.twitch.start())

        # LIVE NOTIFICATION THINGS
        self.is_live = False
        self.ping_channel = None
        self.ping_role = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.ping_channel = helpers.get_chan(self.bot.guild, LIVE_CHANNEL)
        self.ping_role = helpers.get_role(self.bot.guild, "ping me")
        await self.check_if_live()

    async def check_if_live(self):
        while True:
            await asyncio.sleep(300)
            if not self.is_live:
                data = await self.twitch.get_stream(CHANNEL)
                if data:
                    self.is_live = True
                    print(data)
                    await self.send_live_message(data)
                else:
                    self.is_live = False
                    print('is not live')
            else:
                print('is live')

    async def send_live_message(self, data):
        tosend = f'{self.ping_role.mention} {data["user_name"]} is now live'
        link = f'https://www.twitch.tv/{data["user_name"]}'
        await self.ping_channel.send(tosend + " " + link)


def setup(bot):
    bot.add_cog(TwitchBot(bot))
