import atexit
from globals import checkLaunch
from bots import twitchBot

bot = twitchBot.Bot()
task = None

def run():
    task = bot.loop.create_task(bot.start())

@atexit.register
def term():
    checkLaunch.wasLaunched(1)
    checkLaunch.writeLaunched()
