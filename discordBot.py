import discord

from discord.ext import commands


class Raph(commands.Bot):

    def __init__(self, prefix, desc):
        super().__init__(command_prefix=prefix, description=desc)
        self.guild = None
        self.memers = None
        self.peeporunners = None
        self.runnerReaction = None
        self.pingme = None
        self.pingmeReaction = None
        self.roleAssignChannel = None

    async def on_ready(self):
        print('logged in to discord')
        self.guild = discord.utils.find(lambda g: g.name == 'RavenFeet Shareholders', self.guilds)
        self.memers = discord.utils.find(lambda r: r.name == 'memers', self.guild.roles)
        self.peeporunners = discord.utils.find(lambda r: r.name == 'peeporunners', self.guild.roles)
        self.runnerReaction = discord.utils.find(lambda e: e.name == 'peepoRun', self.guild.emojis)
        self.pingme = discord.utils.find(lambda r: r.name == 'ping me', self.guild.roles)
        self.pingmeReaction = discord.utils.find(lambda e: e.name == 'WeHateTwink', self.guild.emojis)
        self.roleAssignChannel = discord.utils.find(lambda c: c.name == 'role-assign', self.guild.channels)
        print(self.guild.name)

    async def on_member_join(self, member):
        if member.guild == self.guild:
            await member.add_roles(self.memers)

    async def on_raw_reaction_add(self, event):
        message = await self.roleAssignChannel.fetch_message(event.message_id)
        reaction = discord.utils.find(lambda r: r.emoji == event.emoji, message.reactions)
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if event.emoji == self.pingmeReaction:
                    await event.member.add_roles(self.pingme)
                    print('ping')
                elif event.emoji == self.runnerReaction:
                    await event.member.add_roles(self.peeporunners)
                    print('run')
                else:
                    await reaction.remove(event.member)
                    print('other')

    async def on_raw_reaction_remove(self, event):
        user = discord.utils.find(lambda u: u.id == event.user_id, self.guild.members)
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if event.emoji == self.pingmeReaction:
                    await user.remove_roles(self.pingme)
                elif event.emoji == self.runnerReaction:
                    await user.remove_roles(self.peeporunners)






