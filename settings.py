import os
from dotenv import load_dotenv
from discord import utils

load_dotenv()

# USED BY BOTH BOTS
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
VERSION = os.getenv("VERSION")

# DISCORD BOT
DISCORD_ID = os.getenv("DISCORD_ID")
SERVER_ID = os.getenv("SERVER_ID")
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE")
ROLE_ASSIGN_CHANNEL = os.getenv("ROLE_ASSIGN_CHANNEL")

# TWITCH BOT
IRC_TOKEN = os.getenv("IRC_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")
TWITCH_ID = os.getenv("TWITCH_ID")
TWITCH_SECRET = os.getenv("TWITCH_SECRET")
NICK = os.getenv("NICK")
CHANNEL = os.getenv("CHANNEL")
TOPICS = os.getenv("TOPICS").split(',')


# DISCORD BOT HELPER FUNCTIONS
def setguild(bot):
    guild = utils.find(lambda g: str(g.id) == SERVER_ID, bot.guilds)
    return guild


def setrole(guild, rolename):
    role = utils.find(lambda r: r.name == rolename, guild.roles)
    return role


def setchan(guild, channame):
    chan = utils.find(lambda c: c.name == channame, guild.channels)
    return chan


def setemote(guild, emotename):
    emote = utils.find(lambda e: e.name == emotename, guild.emojis)
    return emote
