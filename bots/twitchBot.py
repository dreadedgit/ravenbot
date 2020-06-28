from abc import ABC

from twitchio.ext import commands

from globals import settings


class RaphTwitch(commands.Bot, ABC):

    def __init__(self):
        super().__init__(
            irc_token=settings.IRC_TOKEN,
            client_id=settings.TWITCH_ID,
            client_secret=settings.TWITCH_SECRET,
            prefix=settings.COMMAND_PREFIX,
            nick=settings.NICK,
            initial_channels=[settings.CHANNEL]
        )

    async def event_ready(self):
        print(f'Logged into Twitch | {self.nick}')

    async def event_message(self, message):
        pass
