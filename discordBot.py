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

    async def on_reaction_add(self, reaction, user):
        if user.guild == self.guild:
            if reaction.message.channel == self.roleAssignChannel:
                if reaction.emoji == self.pingmeReaction:
                    await user.add_roles(self.pingme)
                elif reaction.emoji == self.runnerReaction:
                    await user.add_roles(self.peeporunners)
                else:
                    await reaction.remove(user)

    async def on_reaction_remove(self, reaction, user):
        if user.guild == self.guild:
            if reaction.message.channel == self.roleAssignChannel:
                if reaction.emoji == self.pingmeReaction:
                    await user.remove_roles(self.pingme)
                elif reaction.emoji == self.runnerReaction:
                    await user.remove_roles(self.peeporunners)






