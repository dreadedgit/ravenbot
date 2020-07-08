import asyncio

from discord.ext import commands

from bots import twitchbot
from settings import helpers

filename = 'cogs/discord/json/livenotif.json'
data = helpers.open_file(filename)
CHANNEL_NAME = data["CHANNEL"]["NAME"]
ROLE_ID = data["ROLE"]["ID"]
TWITCH_CHANNEL = helpers.get_twitch("CHANNELS")[0]
modules = [
    'cogs.twitch.customcommands',
    'cogs.twitch.timers',
    # 'cogs.twitch.basiccommands'
]


class RavenbotTCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitchbot.RavenbotT()
        for m in modules:
            self.twitch.load_module(m)
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
            await asyncio.sleep(120)
            stream = await self.twitch.get_stream(TWITCH_CHANNEL)
            if is_live:
                if stream is not None:
                    print('is live')
                    is_live = True
                else:
                    is_live = False
            else:
                if stream is not None:
                    await self.send_live_message(stream)
                    is_live = True
                else:
                    print('is not live')
                    is_live = False

    async def send_live_message(self, stream):
        link = f'https://www.twitch.tv/{stream["user_name"]}'
        await self.channel.send(f'{self.role.mention} {link}')


def setup(bot):
    bot.add_cog(RavenbotTCog(bot))
