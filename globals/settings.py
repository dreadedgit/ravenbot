import os

from dotenv import load_dotenv

load_dotenv()

# USED BY BOTH BOTS
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
VERSION = os.getenv("VERSION")

# DISCORD BOT
DISCORD_ID = os.getenv("DISCORD_ID")
SERVER_ID = os.getenv("SERVER_ID")
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE")
ROLE_ASSIGN_CHANNEL = os.getenv("ROLE_ASSIGN_CHANNEL")
MEMES_CHANNEL = os.getenv("MEMES_CHANNEL")
LIVE_CHANNEL = os.getenv("LIVE_CHANNEL")

# TWITCH BOT
IRC_TOKEN = os.getenv("IRC_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")
TWITCH_ID = os.getenv("TWITCH_ID")
TWITCH_SECRET = os.getenv("TWITCH_SECRET")
NICK = os.getenv("NICK")
CHANNEL = os.getenv("CHANNEL")
TOPICS = os.getenv("TOPICS").split(',')
