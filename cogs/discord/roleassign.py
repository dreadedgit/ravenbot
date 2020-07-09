from discord import utils
from discord.ext import commands

from settings import helpers

filename = 'cogs/discord/json/roleassign.json'
data = helpers.open_file(filename)
CHANNEL_NAME = data["CHANNEL"]["NAME"]
DEFAULT_ID = data["ROLES"][0]["ID"]


def getrole(bot, e):
    id = 0
    for r in data["ROLES"]:
        if r["EMOTE"] == e:
            id = r["ID"]
            break

    return helpers.get_role(bot, id)


def is_allowed(e):
    allowed = False
    for r in data["ROLES"]:
        if r["EMOTE"] != "None":
            if r["EMOTE"] == e:
                allowed = True
                break
            else:
                allowed = False
    return allowed


class RoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.default_role = None
        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.default_role = helpers.get_role(self.bot, DEFAULT_ID)
        self.channel = helpers.get_channel(self.bot, CHANNEL_NAME)
        await self.message_create()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == helpers.get_guild(self.bot):
            await member.add_roles(self.default_role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.guild_id == helpers.get_guild(self.bot).id:
            if event.channel_id == self.channel.id:
                if not is_allowed(str(helpers.get_emote(self.bot, event.emoji.name))):
                    message = await self.channel.fetch_message(event.message_id)
                    reaction = utils.find(lambda r: r.emoji == event.emoji, message.reactions)
                    await reaction.remove(event.member)
                elif is_allowed(str(helpers.get_emote(self.bot, event.emoji.name))):
                    await event.member.add_roles(getrole(self.bot, str(helpers.get_emote(self.bot, event.emoji.name))))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        user = utils.find(lambda u: u.id == event.user_id, helpers.get_guild(self.bot).members)
        if event.guild_id == helpers.get_guild(self.bot).id:
            if event.channel_id == self.channel.id:
                if is_allowed(str(helpers.get_emote(self.bot, event.emoji.name))):
                    await user.remove_roles(getrole(self.bot, str(helpers.get_emote(self.bot, event.emoji.name))))

    async def message_create(self):
        content = []
        for r in data["ROLES"]:
            if r["EMOTE"] != "None":
                content.append(f'{helpers.get_role(self.bot, r["ID"]).mention}: {r["EMOTE"]}')
        roles = "\n".join(content)
        tosend = f'React to this message for the listed roles \n {roles}'
        message = await self.channel.fetch_message(data["MESSAGE"]["ID"])
        await message.edit(content=tosend)


def setup(bot):
    bot.add_cog(RoleCog(bot))
