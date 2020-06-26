from discord.ext import commands
from discord import utils

import settings


class RoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.memers = None
        self.peeporunners = None
        self.runnerReaction = None
        self.pingme = None
        self.pingmeReaction = None
        self.roleAssignChannel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = settings.setGuild(self.bot)
        self.memers = settings.setRole(self.guild, settings.DEFAULT_ROLE)
        self.peeporunners = settings.setRole(self.guild, settings.SPEEDRUNNER_ROLE)
        self.runnerReaction = settings.setEmote(self.guild, settings.SPEEDRUNNER_EMOTE)
        self.pingme = settings.setRole(self.guild, settings.LIVE_NOTIF_ROLE)
        self.pingmeReaction = settings.setEmote(self.guild, settings.LIVE_NOTIF_EMOTE)
        self.roleAssignChannel = settings.setChan(self.guild, settings.ROLE_ASSIGN_CHANNEL)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == self.guild:
            await member.add_roles(self.memers)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if event.emoji == self.pingmeReaction:
                    await event.member.add_roles(self.pingme)
                    print('ping')
                elif event.emoji == self.runnerReaction:
                    await event.member.add_roles(self.peeporunners)
                    print('run')
                else:
                    message = await self.roleAssignChannel.fetch_message(event.message_id)
                    reaction = utils.find(lambda r: r.emoji == event.emoji, message.reactions)
                    await reaction.remove(event.member)
                    print('other')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        user = utils.find(lambda u: u.id == event.user_id, self.guild.members)
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if event.emoji == self.pingmeReaction:
                    print('remove ping')
                    await user.remove_roles(self.pingme)
                elif event.emoji == self.runnerReaction:
                    print('remove run')
                    await user.remove_roles(self.peeporunners)


def setup(bot):
    bot.add_cog(RoleCog(bot))
