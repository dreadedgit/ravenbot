from concurrent import futures
import logging

import discord
from discord.ext import commands

from ravenbot import config

LOG = logging.getLogger(__name__)

EXTENSIONS = {
    # 'admin',
    # 'help',
    # 'streams'
}


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix="!", **kwargs)

    async def on_ready(self):
        LOG.debug(f"Bot is connected | username: {self.user} | user id: {self.user.id}")
        LOG.debug(f"Guilds: {', '.join(f'{guild.name}#{guild.id}' for guild in self.guilds)}")

    async def on_command(self, ctx):
        _repr = ctx.channel.recipient if isinstance(ctx.channel, discord.DMChannel) \
            else f"{ctx.guild.name}#{ctx.channel.name}"
        LOG.debug(f"[{_repr}] Command called by '{ctx.author.display_name}': '{ctx.message.content}'")

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if not isinstance(error, (commands.CommandOnCooldown, futures.TimeoutError)):
            ctx.command.reset_cooldown(ctx)

        if isinstance(error, commands.MissingRequiredArgument):
            LOG.warning(f"Missing argument in command {ctx.command}: {error.args}")
            await ctx.invoke(self.get_command('help'), command_name=ctx.command.qualified_name)
        elif isinstance(error, commands.CommandOnCooldown):
            LOG.warning(f"'{ctx.author.name}' tried to use the command '{ctx.command.name}' while it "
                        f"was still on cooldown for {round(error.retry_after, 2)}s")
        elif isinstance(error, commands.CheckFailure):
            LOG.error(f"Check failed: {error.args[0]} ({type(error).__name__})")
        else:
            LOG.warning(f"Exception '{type(error).__name__}' raised in command '{ctx.command}'",
                        exc_info=(type(error), error, error.__traceback__))

    async def start(self, *args, **kwargs):
        try:
            token = config['discord']['client_id']
            self.load_extensions()
            await super().start(token, *args, **kwargs)
        except ConnectionError:
            LOG.exception("Cannot connect to the websocket")

    def load_extensions(self):
        """Load all cogs"""

        for extension in EXTENSIONS:
            extension = f"discordbot.cogs.{extension}"
            if extension in self.extensions:
                LOG.debug(f"The extension '{extension}' is already loaded")
                continue
            try:
                self.load_extension(extension)
                LOG.debug(f"The extension '{extension}' has been successfully loaded")
            except (discord.ClientException, ModuleNotFoundError):
                LOG.exception(f"Failed to load extension '{extension}'")