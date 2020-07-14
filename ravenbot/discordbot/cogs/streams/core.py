import logging
import asyncio
import collections

from discord import errors
from discord.ext import commands

from ravenbot.cfg import Config
from ... import api
from ...api import twitch
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
            'game_id': 0,
            'start_time': ''
        }
    }
}


class MissingStreamName(commands.MissingRequiredArgument):

    def __init__(self):
        self.message = 'At least one stream name is required'


class Streams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.streams = config
        if len(self.streams['streams']) == 0:
            self.streams.update(DEFAULT_STREAMS_FILE)
            self.streams.write(filename, DEFAULT_STREAMS_FILE)
        self.client = twitch.TwitchAPIClient(self.bot.loop)
        self.webhook_server = twitch.TwitchWebhookServer(self.bot.loop, self.on_webhook_event)
        self.tasks = []

        self.bot.loop.create_task(self.init())

    def cog_unload(self):
        self.webhook_server.stop()
        for task in self.tasks:
            task.cancel()

    async def init(self):
        await self.webhook_server.start()
        await self.bot.wait_until_ready()

        self.tasks.append(self.bot.loop.create_task(self.update_subscriptions()))

        def task_done_callback(fut):
            if fut.cancelled():
                LOG.debug(f'The task has been cancelled: {fut}')
                return
            error = fut.exception()
            if error:
                LOG.error(f'A task ended unexpectedly: {fut}', exc_info=(type(error), error, error.__traceback__))

        for task in self.tasks:
            task.add_done_callback(task_done_callback)

    async def on_webhook_event(self, topic, timestamp, body):
        """Method called when a webhook event is received"""

        stream_data = body.get('data')
        user_id = topic.params['user_id']

        user_data = (await self.client.get_users(user_ids=[user_id]))[0]

        if stream_data:
            stream_data = stream_data[0]
            active_streams_by_id = self._get_active_streams()
            for a in active_streams_by_id:
                if a == stream_data['user_id']:
                    pass
            if stream_data['type'] != 'live':
                pass
            else:
                self._change_status(stream_data['user_id'])
                await self._on_stream_live(timestamp, user_data, stream_data)
        else:
            await self._on_stream_offline(user_data)

    async def update_subscriptions(self):
        """renew webhook subscriptions"""
        LOG.debug('Subscriptions refresh task running...')
        while True:
            try:
                subscriptions = await self.webhook_server.list_subscriptions()
                subscribed_users_by_id = {sub.topic.params['user_id']: sub for sub in subscriptions}

                missing_subscriptions = set()
                outdated_subscriptions = set()

                for u in self.streams['streams']:
                    if self.streams['streams'][u]['user_id'] not in subscribed_users_by_id:
                        missing_subscriptions.add(twitch.StreamChanged(user_id=self.streams['streams'][u]['user_id']))
                    elif subscribed_users_by_id[self.streams['streams'][u]['user_id']].expires_in < 3600:
                        outdated_subscriptions.add(twitch.StreamChanged(user_id=self.streams['streams'][u]['user_id']))

                if missing_subscriptions:
                    LOG.info(f'No subscription for topics: {missing_subscriptions}')
                if outdated_subscriptions:
                    LOG.info(f'Outdated subscriptions for topics: {outdated_subscriptions}')

                await self.webhook_server.unsubscribe(*outdated_subscriptions)
                await self.webhook_server.subscribe(*missing_subscriptions | outdated_subscriptions)
                await asyncio.sleep(600)
            except api.APIError:
                await asyncio.sleep(10)

    async def _on_stream_live(self, timestamp, user_data, stream_data):
        """call when stream info changes"""
        game_id = stream_data['game_id']
        game = (await self.client.get_games(game_id))[0]['name'] if game_id else game_id
        new_embed = models.NotificationEmbed(
            login=user_data['login'],
            display_name=user_data['display_name'],
            game=game,
            title=stream_data['title'],
            logo=user_data['profile_image_url']
        )

    async def _on_stream_offline(self, user_data):
        """call when stream goes offline"""

        active_streams = self._get_active_streams()

        for a in active_streams:
            if user_data['user_id'] == a:
                self._change_status(user_data)
                break

    def _change_status(self, data):
        user = self.streams['streams'][data['login']]
        print(user)
        self.streams.write(filename, self.streams)

    def _get_active_streams(self):
        active_streams_by_id = []
        for u in self.streams['streams']:
            if u['type']:
                active_streams_by_id.append(u['user_id'])

        return active_streams_by_id
