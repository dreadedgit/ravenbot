import discordBot
import settings

r = discordBot.Raph(settings.COMMAND_PREFIX, settings.VERSION)

# r.load_extension('cogs.twitchCog')
# r.load_extension('cogs.goofCog')
r.load_extension('cogs.roleAssignCog')

r.run(settings.DISCORD_ID)
