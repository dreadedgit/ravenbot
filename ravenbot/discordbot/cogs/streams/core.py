import logging
import asyncio
import collections

from discord import errors
from discord.ext import commands

from datetime import timedelta
from ravenbot.cfg import Config
from ...check import is_admin
from . import models
import main

config = Config()
filename = 'settings/discord/streams.yml'
config.load(filename)

LOG = logging.getLogger(__name__)

DEFAULT_STREAMS_FILE = {
    'streams': {
        'user': {
            'type': '',
            'user_id': 0,
            'start_time': ''
        }
    }
}


class Streams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twitch = None
        self.streams = config
        self.twitch = main.gettwitchbot()
        if len(self.streams['streams']) == 0:
            self.streams.update(DEFAULT_STREAMS_FILE)
            self.streams.write(filename, DEFAULT_STREAMS_FILE)

    @commands.Cog.listener()
    async def on_ready(self):
        await self._check_stream()

    # check if channels in streams.yml are live
    async def _check_stream(self):
        while True:
            for s in self.streams["streams"]:
                user_data = self.streams["streams"][s]
                current_stream = await self.twitch.get_stream(user_data['user_id'])
                # if stream is offline
                if not current_stream:
                    # check if stream was live
                    if user_data['type'] == 'live':
                        # update streams.yml
                        await self._change_status(s, current_stream)
                # if stream is live
                else:
                    # check if stream was live
                    if user_data['type'] == 'live':
                        pass
                    # if stream was not live
                    else:
                        # check when last stream started
                        if self._check_time(user_data, current_stream):
                            await self._send_live_message(current_stream)
                        # update streams.yml regardless of sending message
                        await self._change_status(s, current_stream)
                # wait 2 minutes before checking next stream
                await asyncio.sleep(120)

    async def _change_status(self, user, stream):
        # if updating status for offline stream
        if not stream:
            self.streams['streams'][user]['type'] = ''
        else:
            self.streams['streams'][user]['type'] = 'live'
            self.streams['streams'][user]['start_time'] = stream['started_at']
        self.streams.write(filename, self.streams)

    async def _send_live_message(self, stream):
        pass

    def _check_time(self, user, stream):
        delta = timedelta(user['start_time'] - stream['started_at'])
        if delta.total_seconds() < 600:
            return False
