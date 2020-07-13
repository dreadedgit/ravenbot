import os

import logging
from logging import handlers

from .cfg import Config

config = Config()

# Logger setup
os.makedirs("logs", exist_ok=True)
log_pattern = logging.Formatter("[%(asctime)s][%(levelname)s]: %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# write in the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_pattern)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# write into a file
filepath = f"{os.path.join('logs', 'config')}.log"
file_handler = handlers.RotatingFileHandler(filepath, "a", 1000000, 1, encoding="utf-8")
file_handler.setFormatter(log_pattern)
stream_handler.setLevel(config.get("debug", logging.DEBUG))
logger.addHandler(file_handler)