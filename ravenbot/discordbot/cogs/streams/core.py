import logging
import asyncio
import collections

import discord
from discord import errors
from discord.ext import commands

from datetime import timedelta
from ravenbot.cfg import Config
from ...check import is_admin
from . import models
from main import func

config = Config()
filename = 'settings/discord/streams.yml'
config.load(filename)

LOG = logging.getLogger(__name__)

DEFAULT_STREAMS_FILE = {
    'streams': {
        'user': {
            'type': '',
            'start_time': ''
        }
    },
    'channel_info': {
        'name': '',
        'id': 0
    }
}


class Streams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.role = None
        self.channel = None
        self.streams = config
        if len(self.streams['streams']) == 0:
            self.streams.update(DEFAULT_STREAMS_FILE)
            self.streams.write(filename, DEFAULT_STREAMS_FILE)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.guilds[0]
        self.channel = discord.utils.find(lambda c: c.id == self.streams['channel']['id'], self.guild.channels)
        self.role = discord.utils.find(lambda r: r.id == self.streams['role']['id'], self.guild.roles)
        await self._check_stream()

    # check if channels in streams.yml are live
    async def _check_stream(self):
        while True:
            for s in self.streams["streams"]:
                user_data = (await func.get_users(s))[0]
                current_stream = await func.get_stream(user_data.id)
                # if stream is offline
                if not current_stream:
                    # check if stream was live
                    if self.streams["streams"][s]['type'] == 'live':
                        # update streams.yml
                        await self._change_status(s, current_stream)
                # if stream is live
                else:
                    # check if stream was live
                    if self.streams["streams"][s]['type'] == 'live':
                        pass
                    # if stream was not live
                    else:
                        # check when last stream started
                        if self._check_time(s, current_stream):
                            game_id = current_stream['game_id']
                            game = (await func.get_games(game_id))[0]['name']
                            data = {
                                'user_login': user_data.login,
                                'display_name': user_data.display_name,
                                'title': current_stream['title'],
                                'game': game,
                                'logo': user_data.profile_image
                            }
                            await self._send_live_message(data)
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

    async def _send_live_message(self, data):
        new_embed = models.NotificationEmbed(
            login=data['login'],
            display_name=data['display_name'],
            title=data['title'],
            game=data['game'],
            logo=data['logo']
        )
        await self.channel.send(content=f'{self.role.mention}', embed=new_embed)

    def _check_time(self, user, stream):
        delta = timedelta(self.streams["streams"][user]['start_time'] - stream['started_at'])
        if delta.total_seconds() < 600:
            return False
        else:
            return True
