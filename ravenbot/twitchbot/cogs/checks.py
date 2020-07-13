def has_prefix(message):
    if message.content.startswith('!'):
        return True
    else:
        return False


def is_bot(user, bot):
    if user.name == bot.nick:
        return True
    else:
        return False


def is_mod(user):
    if user.is_mod:
        return True
    else:
        return False
