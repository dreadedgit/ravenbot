import os
from dotenv import load_dotenv

load_dotenv()

# USED BY BOTH BOTS
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
VERSION = os.getenv("VERSION")

# DISCORD BOT
DISCORD_ID = os.getenv("DISCORD_ID")
SERVER_ID = os.getenv("SERVER_ID")

#TWITCH BOT
TWITCH_ID = os.getenv("TWITCH_ID")
IRC_TOKEN = os.getenv("IRC_TOKEN")
NICK = os.getenv("NICK")
CHANNEL = os.getenv("CHANNEL")
TWITCH_SECRET = os.getenv("TWITCH_SECRET")





