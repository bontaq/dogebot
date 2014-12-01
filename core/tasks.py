from celery import task
from core.soundcloud_api import SoundCloudAPI
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
soundcloud = SoundCloudAPI()


@task
def send_welcome(user):
    msg = "Welcome to dogebot, your deposit address is: {address}".format(
        address=user.deposit_address
    )
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Reply: welcomed: %s %s %s', user.user_name, user.user_id, user.deposit_address)
    except Exception as e:
        logger.exception(e)


@task
def send_already_registered(user):
    msg = "You've already registered, your deposit address is: {address} and " \
          "your balance is: {balance}".format(
              address=user.deposit_address,
              balance=user.balance)
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Reply: already registered: %s %s', user.user_name, user.user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_balance(user):
    msg = "Your balance is: {balance} doges".format(
        balance=user.balance.quantize(Decimal("0.00")))
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Reply: balance: %s %s %s',
                    user.user_name,
                    user.user_id,
                    user.balance.quantize(Decimal("0.00")))
    except Exception as e:
        logger.exception(e)


@task
def send_notify_of_tip(from_user, to_user):
    msg = "{from_user} would like to send you a dogecoin tip, reply with 'accept' to " \
          "register and accept this tip.".format(
              from_user=from_user.user_name
          )
    try:
        soundcloud.send_message(to_user.user_id, msg)
        logger.info('Reply: asked user to register.  from_user: {from_user}, to_user: {to_user}',
                    from_user,
                    to_user)
    except Exception as e:
        logger.exception(e)


@task
def send_from_user_not_registered():
    pass


@task
def send_bad_balance():
    pass
