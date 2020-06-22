import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SERVER_ID = os.getenv("SERVER_ID")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
