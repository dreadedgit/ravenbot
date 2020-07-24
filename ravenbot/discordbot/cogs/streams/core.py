import logging
import asyncio
import collections

import discord
from discord import errors
from discord.ext import commands

from datetime import timedelta, date
from ravenbot.cfg import Config
from ...check import is_admin
from . import models
from main import func

config = Config()
filename = 'settings/discord/streams.yml'
config.load(filename)

LOG = logging.getLogger(__name__)


def create_default_file(guilds):
    DEFAULT_STREAMS_FILE = {
        'servers': []
    }
    for g in guilds:
        server = {
            'name': g.name,
            'id': g.id,
            'channel': {
                'name': '',
                'id': 0
            },
            'role': {
                'name': '',
                'id': 0
            },
            'streams': []
        }
        DEFAULT_STREAMS_FILE['servers'].append(server)
    return DEFAULT_STREAMS_FILE


class Streams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.streams = config

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.streams.items():
            self.streams.update(create_default_file(self.bot.guilds))
            self.streams.write(filename, self.streams)
        print(self.streams['servers'])
        # await self._check_stream()

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
        delta = timedelta(date(self.streams["streams"][user]['start_time']) - stream['started_at'])
        if delta.total_seconds() < 600:
            return False
        else:
            return True
