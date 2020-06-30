import json
import sys
import traceback

from twitchio.ext import commands


@commands.cog(name='simple')
class SimpleCog:

    def __init__(self, bot):
        self.bot = bot

        with open('json/customcommands.json') as json_file:
            self.data = json.load(json_file)
        json_file.close()

    def is_command(self, name):
        result = False
        for com in self.data['commands']:
            if name == com["name"]:
                result = True
                break
        return result

    def addcom(self, name, response):
        com = {"name": name, "response": response}
        self.data['commands'].append(com)
        with open('json/customcommands.json', 'w') as outfile:
            json.dump(self.data, outfile)

    def delcom(self, name):
        for com in self.data['commands']:
            if name == com["name"]:
                self.data['commands'].remove(com)
                with open('json/customcommands.json', 'w') as outfile:
                    json.dump(self.data, outfile)
                break

    def getresponse(self, name):
        response = ''
        for com in self.data['commands']:
            if name == com["name"]:
                response = com["response"]
                break
        return response

    @commands.command(name='addcom',
                      aliases='addcommand')
    async def _add_command(self, ctx, name, *response):
        re = ''
        if not ctx.author.is_mod:
            re = f'@{ctx.author.name} only mods can add commands'
        elif ctx.author.is_mod:
            if self.is_command(name):
                re = f'@{ctx.author.name} command with name \"' + name + '\" already exists'
            else:
                full = ' '.join(response)
                self.addcom(name, full)
                re = f'@{ctx.author.name} command with name \"' + name + '\" added'
        await ctx.send(content=re)

    @commands.command(name='delcom',
                      aliases='deletecom')
    async def _del_command(self, ctx, name):
        re = ''
        if not ctx.author.is_mod:
            re = f'@{ctx.author.name} only mods can delete commands'
        elif ctx.author.is_mod:
            if not self.is_command(name):
                re = f'@{ctx.author.name} command with name \"' + name + '\" doesn\'t exist'
            else:
                self.delcom(name)
                re = f'@{ctx.author.name} command with name \"' + name + '\" deleted'
        await ctx.send(content=re)

    async def event_message(self, message):
        if not message.author.name == self.bot.nick:
            if message.content.startswith('!'):
                if self.is_command(message.content.strip('!')):
                    await message.channel.send(content=self.getresponse(message.content.strip('!')))
                else:
                    await self.bot.handle_commands(message)

    async def event_error(self, error, data):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

