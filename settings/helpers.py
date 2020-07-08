import json
import logging

from discord import utils

from utility import logger as _logger

BOTSETTINGS = 'settings/json/botsettings.json'


# JSON HELPER FUNCTIONS
def open_file(file):
    with open(file) as o:
        d = json.load(o)
    o.close()
    return d


def write_file(d, file):
    with open(file, 'w') as o:
        json.dump(d, o, indent=4)
    o.close()


data = open_file(BOTSETTINGS)


# LOGGER HELPER FUNCTION
def setup_logger(name):
    logger = logging.getLogger(name)
    _logger.setup_logger(logger)
    return logger


# TWITCH HELPER FUNCTION
def get_twitch(s):
    return data["TWITCH"][s]


# DISCORD HELPER FUNCTIONS
def get_discord(s):
    return data["DISCORD"][s]


def get_guild(bot):
    guild = utils.find(lambda g: g.id == get_discord("SERVER ID"), bot.guilds)
    return guild


def get_channel(bot, name):
    channel = utils.find(lambda c: c.name == name, get_guild(bot).channels)
    return channel


def get_role(bot, roleid):
    role = utils.find(lambda r: r.id == roleid, get_guild(bot).roles)
    return role


def get_emote(bot, name):
    emote = utils.find(lambda e: e.name == name, get_guild(bot).emojis)
    return emote
