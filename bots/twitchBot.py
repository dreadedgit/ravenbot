# bot.py
import os
from globals import sqlConfig
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[os.environ['CHANNEL']]
        )

    async def event_ready(self):
        print(f"{os.environ['BOT_NICK']} is online")
        self.userData = await self.get_users(os.environ['CHANNEL'])
        self.userID = self.userData[0][0]
        print(self.userID)

bot = Bot()
bot.run()
