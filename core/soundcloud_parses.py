import re
from decimal import Decimal


def is_register(message):
    if message.strip().lower() == 'register':
        return True
    return False


def is_get_balance(message):
    if re.match('^balance$|^get\s?balance$', message.strip(), re.IGNORECASE):
        return True
    return False


tip_regex = 'tip\s(\S+?)\s(\d+\.\d+|\d+)$'


def is_tip(message):
    if re.match(tip_regex, message.strip(), re.IGNORECASE):
        return True
    return False


def parse_tip(message):
    match = re.match(tip_regex, message.strip(), re.IGNORECASE)
    if match:
        return match.group(1, 2)
    return None, None


def is_mention_tip(message):
    if re.match('^@dogebot: tip (\d+)$', message.strip(), re.IGNORECASE):
        return True
    return False


def parse_mention_tip(message):
    match = re.match('^@dogebot: tip (\d+\.\d+|\d+)$', message.strip(), re.IGNORECASE)
    return Decimal(match.group(1))
