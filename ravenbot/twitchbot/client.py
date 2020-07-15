import collections
from abc import ABC
import logging

import twitchio
from twitchio.ext import commands
from ravenbot import config

LOG = logging.getLogger(__name__)

EXTENSIONS = {
    'timers',
    'custom',
    # 'quotes',
    # 'mod',
    # 'stock',
    'followage'
}


class Bot(commands.Bot, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(
            irc_token=config["twitch"]["irc_token"],
            prefix="!",
            nick=config["twitch"]["nick"],
            initial_channels=config["twitch"]["channels"],
            client_secret=config["twitch"]["client_secret"],
            client_id=config["twitch"]["client_id"],
        )

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_ready(self):
        LOG.debug(f"Bot is connected | username: {self.nick}")

    async def event_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""

        if hasattr(ctx.command, 'event_error'):
            return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            LOG.warning(f"Missing argument in command {ctx.command}: {error.args}")
        elif isinstance(error, commands.CheckFailure):
            LOG.error(f"Check failed: {error.args[0]} ({type(error).__name__})")
        else:
            LOG.warning(f"Exception '{type(error).__name__}' raised in command '{ctx.command}'",
                        exc_info=(type(error), error, error.__traceback__))

    async def start(self):
        try:
            self.load_extensions()
            await super().start()
        except ConnectionError:
            LOG.exception("Cannot connect to the websocket")

    def load_extensions(self):
        """Load all cogs"""

        for extension in EXTENSIONS:
            extension = f"twitchbot.cogs.{extension}"
            if extension in self.cogs:
                LOG.debug(f"The extension '{extension}' is already loaded")
                continue
            try:
                self.load_module(extension)
                LOG.debug(f"The extension '{extension}' has been successfully loaded")
            except (twitchio.errors.ClientError, ModuleNotFoundError):
                LOG.exception(f"Failed to load extension '{extension}'")
