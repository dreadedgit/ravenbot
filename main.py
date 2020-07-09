from bots import discordbot
from settings import helpers

raph = discordbot.Ravenbot()

cogs = ['cogs.discord.twitchcog', 'cogs.discord.roleassign']


for c in cogs:
    raph.load_extension(c)

raph.run(helpers.get_discord("CLIENT ID"))
