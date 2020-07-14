import logging
import asyncio
import collections

from discord import errors
from discord.ext import commands

from ravenbot.cfg import Config
from ...check import is_admin
from . import models


config = Config()
filename = 'settings/discord/streams.yml'
config.load(filename)

LOG = logging.getLogger(__name__)

DEFAULT_STREAMS_FILE = {
    'streams': {
        'user': {
            'type': '',
            'stream_id': 0,
            'user_id': 0,
            'start_time': ''
        }
    }
}


class Streams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = twitch
        self.streams = config
        if len(self.streams['streams']) == 0:
            self.streams.update(DEFAULT_STREAMS_FILE)
            self.streams.write(filename, DEFAULT_STREAMS_FILE)

    @commands.Cog.listener()
    async def on_ready(self):
        await self._check_stream()

    async def _check_stream(self):
        while True:
            for s in self.streams["streams"]:
                current_stream = self.twitch.get_stream(s.get('user_id'))
                if not current_stream:
                    if s.get('type') == 'live':
                        await self._change_status(s, current_stream)
                else:
                    if s.get('type') == 'live':
                        pass
                    else:
                        await self._change_status(s, current_stream)

    async def _change_status(self, user, stream):
        pass

    async def _send_live_message(self, stream):
        pass
