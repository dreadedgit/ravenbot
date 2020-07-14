import discord

TWITCH_ICON_URL = "https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png"

ONLINE_COLOR = discord.Color.dark_purple()


class NotificationEmbed(discord.Embed):

    def __init__(self, login, display_name, title, game, logo=None):
        super().__init__()

        channel_url = f"https://www.twitch.tv/{login}"
        self.set_author(name=display_name, url=channel_url, icon_url=TWITCH_ICON_URL)
        self.description = channel_url

        self.add_field(name="Title", value=title or "No Title", inline=False)
        self.add_field(name="Game", value=game or "No Game", inline=False)

        if logo:
            self.set_thumbnail(url=logo)

        self.color = ONLINE_COLOR
