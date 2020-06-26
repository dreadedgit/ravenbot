from abc import ABC

from twitchio.ext import commands

import settings
import json


def appendID(t, cid):
    new = t + '.' + str(cid)
    return new


class RaphTwitch(commands.Bot, ABC):

    def __init__(self):
        super().__init__(
            irc_token=settings.IRC_TOKEN,
            client_id=settings.TWITCH_ID,
            client_secret=settings.TWITCH_SECRET,
            prefix=settings.COMMAND_PREFIX,
            nick=settings.NICK,
            initial_channels=[settings.CHANNEL]
        )
        self.channel = None
        self.topics = settings.TOPICS
        self.pubsubTopics = []

    async def event_ready(self):
        print(f'Logged into Twitch | {self.nick}')
    #     self.channel = await self.get_users('dreaded_')
    #     cid = self.channel[0].id
    #
    #     for t in self.topics:
    #         temp = appendID(t, cid)
    #         self.pubsubTopics.append(temp)
    #
    #     await self.pubsub_subscribe(settings.API_TOKEN, *self.pubsubTopics)
    #
    # async def event_raw_pubsub(self, data):
    #     print(data)

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name='socials')
    async def social_message(self, ctx):
        await ctx.send('Twitter: https://twitter.com/dreadedrta')
        await ctx.send('Discord: https://discord.gg/X2fsxAM')

    # @commands.command(name='addcom')
    # async def make_custom_command(self, ctx, *args):
    #     if ctx.author.is_mod & len(args) > 1:
    #
    #         custom_command = {'name': }


