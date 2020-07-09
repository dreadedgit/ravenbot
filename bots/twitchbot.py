import sys
import traceback
from abc import ABC

from twitchio.ext import commands

from settings import helpers


class RavenbotT(commands.Bot, ABC):

    def __init__(self):
        super().__init__(
            irc_token=helpers.get_twitch("IRC TOKEN"),
            client_id=helpers.get_twitch("CLIENT ID"),
            client_secret=helpers.get_twitch("CLIENT SECRET"),
            prefix=helpers.get_twitch("COMMAND PREFIX"),
            nick=helpers.get_twitch("NICKNAME"),
            initial_channels=helpers.get_twitch("CHANNELS")
        )
        self.logger = helpers.setup_logger(__name__)

    async def event_ready(self):
        self.logger.info(f'Logged into Twitch | {self.nick}')
        for c in helpers.get_twitch("CHANNELS"):
            await self.get_channel(c).colour('CadetBlue')

    async def event_message(self, message):
        self.logger.log(5, f'{message.author.name}: {message.content}')
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
