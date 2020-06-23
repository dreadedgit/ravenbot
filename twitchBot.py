from twitchio.ext import commands

import settings


class RaphTwitch(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=settings.IRC_TOKEN,
            client_id=settings.TWITCH_ID,
            client_secret=settings.TWITCH_SECRET,
            nick=settings.NICK,
            prefix=settings.COMMAND_PREFIX,
            initial_channels=[settings.CHANNEL])

    async def event_ready(self):
        print(f'Logged into Twitch | {self.nick}')

    async def event_message(self, message):
        print('TWITCH LOG:', message.author.name, ':', message.content)
        await self.handle_commands(message)

    @commands.command(name='socials')
    async def social_message(self, ctx):
        await ctx.send('Twitter: https://twitter.com/dreadedrta')
        await ctx.send('Discord: https://discord.gg/X2fsxAM')

    @commands.command(name='ban')
    async def ban_command(self, ctx, *args):
        if len(args) > 1:
            to_ban = args[0]
            new_args = []
            for a in args:
                if a == to_ban:
                    continue
                new_args.append(a)
            if new_args[0] == 'for':
                del new_args[0]
            message = ' '.join(new_args)
            await ctx.send(to_ban + ' has been banned for ' + message)
        else:
            await ctx.send('USAGE: !ban {user} {reason}')