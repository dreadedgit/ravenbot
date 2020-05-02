from discord.ext import commands
from globals import sqlConfig

class UpdateCog(commands.Cog):

    def __init__(self, bot):
        self.discord_bot = bot
        self.dbase = sqlConfig.sqldbase

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):


        for e in before:
            if e not in after:
                removed.append(e)
        for e in after:
            if e not in before:
                added.append(e)

        for e in added:
            if e.animated is True:
                fullemote = '<a:' + str(e.name).replace('\'', '') + ':' + str(e.id) + '>'
            else:
                fullemote = '<:' + str(e.name) + ':' + str(e.id) + '>'

            emoteInfo = [str(e.name), str(e.id), fullemote, str(guild.id)]
            self.dbase.dataInsert('demotes', sqlConfig.dEmotes, emoteInfo)

        for e in removed:
            self.dbase.deleteEntry('demotes', 'emoteID', str(e.id))



def setup(bot):
    bot.add_cog(UpdateCog(bot))
