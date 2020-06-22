import discordBot
import settings

r = discordBot.Raph(settings.COMMAND_PREFIX, settings.VERSION)


r.run(settings.CLIENT_ID)
