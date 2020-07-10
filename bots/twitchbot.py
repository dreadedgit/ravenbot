from abc import ABC

from twitchio.ext import commands

from settings.helpers import get_twitch
from utility import logger as logging


class RavenbotT(commands.Bot, ABC):

    def __init__(self):
        super().__init__(
            irc_token=get_twitch("IRC TOKEN"),
            client_id=get_twitch("CLIENT ID"),
            client_secret=get_twitch("CLIENT SECRET"),
            prefix=get_twitch("COMMAND PREFIX"),
            nick=get_twitch("NICKNAME"),
            initial_channels=get_twitch("CHANNELS")
        )
        self.logger = None
        self.cooldown = False
        self.tosend = ''
        self.previous = ''
        self.count = 0

    async def event_ready(self):
        self.logger = logging.get_logger(__name__)
        logging.setup_logger(self.logger)
        self.logger.info(f'Logged into Twitch | {self.nick}')
        for c in get_twitch("CHANNELS"):
            await self.get_channel(c).colour('CadetBlue')
