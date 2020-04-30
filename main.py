import os
import atexit

from bots import discordBot
from globals import checkLaunch
from discord.ext import commands

checkLaunch.createDBase()

dHelp = commands.DefaultHelpCommand()
bot = discordBot.dBot(command_prefix=os.environ['BOT_PREFIX'], help_command=dHelp, description='RavenBot v0.1')

bot.load_extension("cogs.twitchCog")

bot.run(os.environ['DISCORD_ID'])

@atexit.register
def term():
    checkLaunch.wasLaunched(1)
    checkLaunch.writeLaunched()
    bot.logout()
