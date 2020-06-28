import discordBot
import settings

r = discordBot.Raph(settings.COMMAND_PREFIX, settings.VERSION)

r.load_extension('cogs.discordcogs.twitchCog')
# r.load_extension('cogs.discordcogs.goofCog')
r.load_extension('cogs.discordcogs.roleAssignCog')

r.run(settings.DISCORD_ID)
