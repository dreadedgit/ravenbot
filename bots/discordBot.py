import discord
from globals import checkLaunch
from globals import twitch
from discord.ext import commands

class dBot(commands.Bot):

    async def on_ready(self):
        if checkLaunch.popDBase():
            for guild in self.guilds:
                serverInfo = [str(guild.name).replace('\'', ''), str(guild.id)]
                sqlConfig.sqldbase.dataInsert('dservers', sqlConfig.dServers, serverInfo)
                for emote in guild.emojis:
                    if emote.animated is True:
                        fullemote = '<a:' + str(emote.name).replace('\'', '') + ':' + str(emote.id) + '>'
                    else:
                        fullemote = '<:' + str(emote.name) + ':' + str(emote.id) + '>'

                    emoteInfo = [str(emote.name), str(emote.id), fullemote, str(guild.id)]
                    sqlConfig.sqldbase.dataInsert('demotes', sqlConfig.dEmotes, emoteInfo)
                for channel in guild.channels:
                    channelInfo = [str(channel.name), str(channel.id), str(channel.type), str(guild.id)]
                    sqlConfig.sqldbase.dataInsert('dchannels', sqlConfig.dChannels, channelInfo)
                for role in guild.roles:
                    roleInfo = [str(role.name), str(role.id), str(guild.id)]
                    sqlConfig.sqldbase.dataInsert('droles', sqlConfig.dRoles, roleInfo)
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    webhookInfo = [str(webhook.name), str(webhook.id), str(guild.id)]
                    sqlConfig.sqldbase.dataInsert('dwebhooks', sqlConfig.dWebHooks, webhookInfo)

            sqlConfig.sqldbase.cleanUp()

        print('=---------------------------=')
        print('= logged into discord as')
        print('= ' + self.user.name)
        print('= ' + str(self.user.id))
        print('=---------------------------=')
        print('= logged into twitch as')
        print('= ' + twitch.bot.nick)
