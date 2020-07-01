import sys
import traceback

from discord import utils
from discord.ext import commands

from globals import helpers
from globals.settings import ROLE_ASSIGN_CHANNEL


class RoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.default = None
        self.roleAssignChannel = None
        self.logger = helpers.setup_logger(__name__)

        self.data = helpers.open_file('roleassign')

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = helpers.get_guild(self.bot)
        self.default = helpers.get_default_role(self.guild)
        self.roleAssignChannel = helpers.get_chan(self.guild, ROLE_ASSIGN_CHANNEL)

    def setreaction(self, emote, role):
        reaction = {
            "roleid": helpers.get_role(self.guild, role).id,
            "emotename": emote,
            "name": role
        }
        self.data['reactions'].append(reaction)
        helpers.write_file('roleassign')

    def is_reaction(self, term):
        result = False
        for re in self.data['reactions']:
            if helpers.get_role(self.guild, term) is not None:
                if re["roleid"] == helpers.get_role(self.guild, term).id:
                    result = True
                    break
            elif re["emotename"] == str(term):
                result = True
                break
        return result

    def remove_reaction(self, term):
        for re in self.data['reactions']:
            if helpers.get_role(self.guild, term) is not None:
                if re["roleid"] == helpers.get_role(self.guild, term).id:
                    self.data['reactions'].remove(re)
            elif re["emotename"] == term:
                self.data['reactions'].remove(re)
        helpers.write_file('roleassign')

    def getrole(self, e):
        r = ''
        for re in self.data['reactions']:
            if re["emotename"] == e:
                r = re["name"]
                break

        return helpers.get_role(self.guild, r)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == self.guild:
            await member.add_roles(self.default)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if self.is_reaction(str(event.emoji)):
                    await event.member.add_roles(self.getrole(str(event.emoji)))
                else:
                    message = await self.roleAssignChannel.fetch_message(event.message_id)
                    reaction = utils.find(lambda r: r.emoji == event.emoji, message.reactions)
                    await reaction.remove(event.member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        user = utils.find(lambda u: u.id == event.user_id, self.guild.members)
        if event.guild_id == self.guild.id:
            if event.channel_id == self.roleAssignChannel.id:
                if self.is_reaction(str(helpers.get_emote(self.guild, event.emoji.name))):
                    await user.remove_roles(self.getrole(str(helpers.get_emote(self.guild, event.emoji.name))))

    @commands.command(name="addreaction",
                      pass_context=True,
                      brief="creates a link between given role and emote")
    @commands.has_permissions(manage_roles=True)
    async def _add_reaction(self, ctx, r, e):
        if not self.is_reaction(e):
            self.setreaction(e, r)
            await ctx.send(content="role association added", delete_after=1)
        else:
            await ctx.send(content="association with " + str(e) + " or " + r
                           + " already exists, use !delreaction " + str(e)
                           + " or \"" + r + "\" to remove it", delete_after=1)
        await ctx.message.delete()

    @_add_reaction.error
    async def add_error(self, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            self.logger.error(f"{error}")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="delreaction",
                      pass_context=True,
                      brief="deletes association with given role or emote")
    @commands.has_permissions(manage_roles=True)
    async def _del_reaction(self, ctx, arg):
        if self.is_reaction(arg):
            self.remove_reaction(arg)
            await ctx.send(content="role association deleted", delete_after=1)
        else:
            await ctx.send(content="no association found", delete_after=1)
        await ctx.message.delete()

    @_del_reaction.error
    async def del_error(self, error, ctx):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            self.logger.error(f"{error}")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="message",
                      pass_context=True,
                      brief="create the role assign message")
    @commands.has_permissions(manage_roles=True)
    async def message_create(self, ctx):
        if self.data["message"][0]["messageid"] == 0:
            message = await ctx.send("working")
            self.data["message"][0]["messageid"] = message.id
            helpers.write_file('roleassign')
        message = await self.roleAssignChannel.fetch_message(self.data["message"][0]["messageid"])
        content = []
        for re in self.data["reactions"]:
            content.append("@" + re["name"] + ": " + re["emotename"])
        tosend = self.data["message"][0]["messagecontent"] + "\n" + "\n".join(content)
        await message.edit(content=tosend)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(RoleCog(bot))
