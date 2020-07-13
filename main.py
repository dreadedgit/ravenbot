#!/usr/bin/python

import sys

from ravenbot.discordbot import client as disc
from ravenbot.twitchbot import client as twitch
from ravenbot import config, utils

DEFAULT_CONFIG = {
    "discord": {
        "client_id": "NULL",
        "desc": "NULL"
    },
    "twitch": {
        "irc_token": "NULL",
        "client_id": "NULL",
        "client_secret": "NULL",
        "nick": "NULL",
        "channels": ["NULL"],
        "api_oauth_token": "NULL",
        "api_token": "NULL",
        "api_client_id": "NULL",
        "refresh_token": "NULL",
        "pubsub_topics": ["NULL"]
    }
}

filename = 'settings/config.yml'


def main():
    config.load(filename)
    if len(config) == 0:
        config.update(DEFAULT_CONFIG)
        config.write(filename, DEFAULT_CONFIG)
        print("TERMINATING BOT PLEASE UPDATE CONFIG.YML IN SETTINGS FOLDER")
        exit()

    sys.path.append(utils.get_project_name())

    discord = disc.Bot()
    twitchbot = twitch.Bot()

    discord.loop.create_task(twitchbot.start())
    discord.loop.create_task(discord.start())
    discord.loop.run_forever()


if __name__ == "__main__":
    main()
