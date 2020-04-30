import os
import atexit

from bots import discordBot
from globals import checkLaunch
from discord.ext import commands

checkLaunch.createDBase()

dHelp = commands.DefaultHelpCommand()
bot = discordBot.dBot(command_prefix=os.environ['BOT_PREFIX'], help_command=dHelp, description='RavenBot v0.1')

bot.load_extension("cogs.twitchCog")

bot.run('NjIxNTU2MTk4Mzc4MDQ1NDQw.XiJ_Wg.Z4wQgqZFNA1fUH3k_mT-LiwhtAs')

@atexit.register
def term():
    checkLaunch.wasLaunched(1)
    checkLaunch.writeLaunched()
    bot.logout()
