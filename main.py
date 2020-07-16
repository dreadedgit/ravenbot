#!/usr/bin/python

import sys
from typing import Union

from ravenbot.discordbot import client as disc
from ravenbot.twitchbot import client as twitch
from ravenbot import config, utils

if __name__ == "__main__":
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
    config.load(filename)
    if len(config) == 0:
        config.update(DEFAULT_CONFIG)
        config.write(filename, DEFAULT_CONFIG)
        print("TERMINATING BOT PLEASE UPDATE CONFIG.YML IN SETTINGS FOLDER")
        exit()
    sys.path.append(utils.get_project_name())
    _discord = disc.Bot()

_twitchbot = twitch.Bot()


def main():
    _discord.loop.create_task(_twitchbot.start())
    _discord.loop.create_task(_discord.start())
    _discord.loop.run_forever()


if __name__ == "__main__":
    main()


class Utils:

    async def get_users(self, *users: Union[str, int]) -> list:
        data = await _twitchbot.get_users(*users)
        return data

    async def get_stream(self, channel: Union[int, str]):
        data = await _twitchbot.get_stream(channel)
        return data

    async def get_games(self, *games: Union[str, int]):
        data = await _twitchbot.get_games(*games)
        return data


func = Utils()
