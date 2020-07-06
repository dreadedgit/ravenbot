import asyncio

from discord.ext import commands

from bots import twitchbot
from settings import helpers

filename = 'cogs/discord/json/livenotif.json'
data = helpers.open_file(filename)
CHANNEL_NAME = data["CHANNEL"]["NAME"]
ROLE_ID = data["ROLE"]["ID"]
TWITCH_CHANNEL = helpers.get_twitch("CHANNELS")[0]


class RavenbotTCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitchbot.RavenbotT()
        self.twitch.load_module('cogs.twitch.customcommands')
        self.twitch.load_module('cogs.twitch.timers')
        self.twitch.loop.create_task(self.twitch.start())
        self.channel = None
        self.role = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = helpers.get_channel(self.bot, CHANNEL_NAME)
        self.role = helpers.get_role(self.bot, ROLE_ID)
        await self.check_if_live()

    async def check_if_live(self):
        is_live = False
        while True:
            await asyncio.sleep(300)
            if not is_live:
                stream = await self.twitch.get_stream(TWITCH_CHANNEL)
                if stream:
                    is_live = True
                    print(stream)
                    await self.send_live_message(stream)
                else:
                    is_live = False
                    print('is not live')
            else:
                print('is live')

    async def send_live_message(self, stream):
        tosend = f'{self.role.mention} {stream["user_name"]} is now live'
        link = f'https://www.twitch.tv/{stream["user_name"]}'
        await self.channel.send(tosend + " " + link)


def setup(bot):
    bot.add_cog(RavenbotTCog(bot))
