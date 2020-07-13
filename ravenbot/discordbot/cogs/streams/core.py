import asyncio
import collections
from datetime import datetime
import logging

from discord import errors
from discord.ext import commands

from ... import api
from ...api import twitch
from ...check import is_admin

LOG = logging.getLogger(__name__)

RECENT_NOTIFICATION_AGE = 300


class MissingStreamName(commands.MissingRequiredArgument):

    def __init__(self):
        self.message = "At least one stream name is required"


class StreamCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
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
        self.tasks.append(self.bot.loop.create_task(self.delete_old_notifications()))

        def task_done_callback(fut):
            if fut.cancelled():
                LOG.debug(f"The task has been cancelled: {fut}")
                return
            error = fut.exception()
            if error:
                LOG.error(f"A task ended unexpectedly: {fut}", exc_info=(type(error), error, error.__traceback__))

        for task in self.tasks:
            task.add_done_callback(task_done_callback)

    async def on_webhook_event(self, topic, timestamp, body):
        """Method called when a webhook event is received"""

        stream_data = body.get('data')
        user_id = topic.params['user_id']

        # Enrich user data
        user_data = (await self.client.get_users(user_ids=[user_id]))[0]

        if stream_data:
            stream_data = stream_data[0]

            await self._on_stream_update(timestamp, user_data, stream_data)

            # Make sure that any previous stream entry is has an end date