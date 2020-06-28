from bots import discordBot
from globals import settings

r = discordBot.Raph(settings.COMMAND_PREFIX, settings.VERSION)

r.load_extension('discordcogs.twitchCog')
# r.load_extension('discordcogs.goofCog')
r.load_extension('discordcogs.roleAssignCog')

r.run(settings.DISCORD_ID)
