from bots import twitchBot

bot = twitchBot.Bot()
task = None

def run():
    task = bot.loop.create_task(bot.start())
