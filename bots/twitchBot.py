# bot.py
import os
from globals import sqlConfig
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.getenv('TMI_TOKEN'),
            client_id=os.getenv('CLIENT_ID'),
            nick=os.getenv('BOT_NICK'),
            prefix=os.getenv('BOT_PREFIX'),
            initial_channels=[os.getenv('CHANNEL')]
        )

    async def event_ready(self):
        print(f"{os.getenv('BOT_NICK')} is online")
        self.userData = await self.get_users(os.getenv('CHANNEL'))
        self.userID = self.userData[0][0]
        print(self.userID)
