from twitchio.ext import commands


@commands.cog()
class Followage:

    def __init__(self, bot):
        self.bot = bot

    async def get_follow(self, ctx, user_data):
        if len(user_data) == 1:
            tosend = f"@{ctx.author.name} you cannot follow yourself"
        elif len(user_data) == 2:
            follow = await self.bot.get_follow(user_data[0].id, user_data[1].id)
            date = self.format_date(follow["followed_at"].split("T")[0])
            tosend = f"@{ctx.author.name} has been following {ctx.channel.name} since {date}"
        else:
            tosend = 'error'
        await ctx.send(tosend)

    @commands.command()
    async def followage(self, ctx):
        user_data = await self.bot.get_users(ctx.author.name, ctx.channel.name)
        await self.get_follow(ctx, user_data)

