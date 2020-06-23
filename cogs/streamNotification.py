import re
import httplib2
import json
import datetime

from dotenv import load_dotenv
from discord.ext import commands


class StreamNotification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(StreamNotification(bot))
