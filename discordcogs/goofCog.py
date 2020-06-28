import json

from discord.ext import commands

from globals import settings


class GoofCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.memesChannel = None
        self.emotechannel = None

        self.data = {}
        with open('json/goof.json') as json_file:
            self.data = json.load(json_file)
        json_file.close()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = settings.setguild(self.bot)
        self.memesChannel = settings.setchan(self.guild, settings.MEMES_CHANNEL)
        self.emotechannel = settings.setchan(self.guild, self.data["channel"][0]["channelname"])

    # @commands.command(name="setemote",
    #                   pass_context=True,
    #                   brief="sets allowed emote for the emote spam channel")
    # @commands.has_permissions(manage_channels=True)
    # async def _set_channel(self, ctx, e):
    #     if self.data["channel"][0]["channelname"] == 0:
    #         self.data["channel"][0]["channelname"] = ctx.channel.id
    #     elif self.data["channel"][0]["channelname"] == ctx.channel.id:
    #         await ctx.channel.edit(name=settings.setemote())


def setup(bot):
    bot.add_cog(GoofCog(bot))

