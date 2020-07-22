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


def is_vip(user):
    if 'vip' in user.badges:
        return True
    else:
        return False


def check_all(user, message, bot):
    if is_bot(user, bot):
        return True
    else:
        if is_mod(user):
            return True
        else:
            if is_vip(user):
                return True
            else:
                if has_prefix(message):
                    return True
                else:
                    return False
