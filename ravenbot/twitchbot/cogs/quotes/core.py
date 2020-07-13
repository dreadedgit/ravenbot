from twitchio.ext import commands
from ravenbot import Config

config = Config()
DEFAULT_QUOTES_FILE = {
    "quotes": []
}

filename = 'settings/twitch/quotes.yml'


@commands.cog()
class Quotes:

    def __init__(self, bot):
        self.bot = bot
        self.quotes = config
        if len(self.quotes) == 0:
            self.quotes.update(DEFAULT_QUOTES_FILE)
            self.quotes.write(filename, DEFAULT_QUOTES_FILE)


def prep(bot):
    config.load(filename)
    quotes = Quotes(bot)
    bot.add_cog(quotes)
