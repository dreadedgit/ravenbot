import os
import atexit

from bots import discordBot
from globals import sqlConfig
from discord.ext import commands


def wasLaunched(n):
    global _l
    _l = n

try:
    with open("launched") as infile:
        _l = int(infile.read())
        if _l == 0:
            sqlConfig.runOnFirstStart()
except FileNotFoundError:
    _l = '0'

dHelp = commands.DefaultHelpCommand()
bot = discordBot.dBot(command_prefix=os.environ['BOT_PREFIX'], help_command=dHelp, description='RavenBot v0.1')

bot.load_extension("cogs.twitchCog")

bot.run(os.environ['DISCORD_ID'])

def writeLaunched():
    with open("launched", "w") as outfile:
        outfile.write("%d" % _l)

@atexit.register
def term():
    wasLaunched(1)
    writeLaunched()
    bot.logout()
