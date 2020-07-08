from twitchio.ext import commands

from settings import helpers

TWITCH_CHANNEL = helpers.get_twitch("CHANNELS")[0]


@commands.cog()
class BasicCommands:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="followage")
    async def follow_com(self, ctx, *args):
        if len(args) == 1:
            new = [
                args[0],
                ctx.channel.name
            ]
        elif len(args) >= 2:
            new = [
                args[0],
                args[1]
            ]
        else:
            new = [
                ctx.author.name,
                ctx.channel.name
            ]
        user_data = await self.bot.get_users(new[0], new[1])
        follow = await self.bot.get_follow(user_data[0].id, user_data[1].id)
        if follow is not None:
            print(follow)
        else:
            # await ctx.send(f'{new[0]} is not following {new[1]}')
            print('test')


def setup(bot):
    bot.add_cog(BasicCommands(bot))
