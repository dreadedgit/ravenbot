import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_ID = os.getenv("DISCORD_ID")
SERVER_ID = os.getenv("SERVER_ID")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
VERSION = os.getenv("VERSION")
NICK = os.getenv("NICK")
IRC_TOKEN = os.getenv("IRC_TOKEN")
CHANNEL = os.getenv("CHANNEL")
