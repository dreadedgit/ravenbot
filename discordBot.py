import discord
import settings

from discord.ext import commands


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(description=desc, command_prefix=prefix)

    async def on_ready(self):
        print('logged in to discord')

    async def on_message(self, message):
        if message.guild.id == settings.SERVER_ID:
            if message.channel.id == settings.YEP:
                for e in message.guild.emojis:
                    if e.name == 'YEP':
                        await message.channel.send(str(e))
                    else:
                        await self.process_commands(message)
