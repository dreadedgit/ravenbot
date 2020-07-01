from abc import ABC

from twitchio.ext import commands

from globals import helpers
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
        self.logger = helpers.setup_logger(__name__)

    async def event_ready(self):
        self.logger.info(f'Logged into Twitch | {self.nick}')
        await self.get_channel(settings.CHANNEL).colour('CadetBlue')

    async def event_message(self, message):
        self.logger.log(5, f'{message.author.name}: {message.content}')
