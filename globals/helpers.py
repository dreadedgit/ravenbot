import json
import logging

from discord import utils

from globals import logger as _logger
from globals.settings import SERVER_ID, DEFAULT_ROLE


# LOGGER HELPER FUNCTION
def setup_logger(name):
    logger = logging.getLogger(name)
    _logger.setup_logger(logger)
    return logger


# JSON HELPER FUNCTIONS
def open_file(file):
    with open('json/' + file + '.json') as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


def write_file(data, file):
    with open('json/' + file + '.json', 'w') as outfile:
        json.dump(data, outfile)


# DISCORD BOT HELPER FUNCTIONS
def get_guild(bot):
    guild = utils.find(lambda g: str(g.id) == SERVER_ID, bot.guilds)
    return guild


def get_role(guild, rolename):
    role = utils.find(lambda r: r.name == rolename, guild.roles)
    return role


def get_default_role(guild):
    role = utils.find(lambda r: r.id == DEFAULT_ROLE, guild.roles)
    return role


def get_chan(guild, channame):
    chan = utils.find(lambda c: c.name == channame, guild.channels)
    return chan


def get_emote(guild, emotename):
    emote = utils.find(lambda e: e.name == emotename, guild.emojis)
    return emote
