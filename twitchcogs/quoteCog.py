from globals.jsonFunctions import open_file, write_file
from twitchio.ext import commands


@commands.cog(name="quotes")
class QuoteCog:

    def __init__(self, bot):
        self.bot = bot

        self.data = open_file('quotes')
