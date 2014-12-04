from celery import task
from core.soundcloud_api import SoundCloudAPI
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
soundcloud = SoundCloudAPI()


@task
def send_welcome(user):
    msg = "Welcome to dogebot, your deposit address is:\n{address}".format(
        address=user.deposit_address
    )
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Reply: welcomed: %s %s %s', user.user_name, user.user_id, user.deposit_address)
    except Exception as e:
        logger.exception(e)


@task
def send_already_registered(user):
    msg = "You've already registered, your deposit address is:\n{address}\nand " \
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
def send_tip_success(from_user_id, to_user_id, amt):
    from_user = soundcloud.get_soundcloud_user(user_id=from_user_id)
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    quantized_amt = amt.quantize(Decimal("0.00"))

    tip_receiver_msg = "{username} has sent you a tip of {amt} doge".format(
        username=from_user['username'],
        amt=quantized_amt
    )
    tip_sender_msg = "You successfully tipped {amt} doge to {username}".format(
        username=to_user['username'],
        amt=quantized_amt
    )
    try:
        soundcloud.send_message(to_user['id'], tip_receiver_msg)
        soundcloud.send_message(from_user['id'], tip_sender_msg)
    except Exception as e:
        logger.exception(e)


@task
def send_notify_of_tip(from_user, to_user):
    from_user = soundcloud.get_soundcloud_user(user_id=from_user_id)
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = "{from_user} would like to send you a dogecoin tip, reply with 'accept' to " \
          "register and accept this tip.".format(
              from_user=from_user['username']
          )
    try:
        soundcloud.send_message(to_user['id'], msg)
        logger.info('Reply: asked user to register.  from_user: {from_user}, to_user: {to_user}',
                    from_user,
                    to_user)
    except Exception as e:
        logger.exception(e)


@task
def send_notify_from_user_pending_tip(from_user, to_user, amt):
    from_user = soundcloud.get_soundcloud_user(user_id=from_user_id)
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = ("You sent {to_user} a tip of {amt}, they aren't current registered but I'll "
           "let you know if they accept the tip.").format(
               to_user=to_user['username'],
               amt=amt.quantize(Decimal("0.00")))
    try:
        pass
    except Exception as e:
        logger.exception(e)


@task
def send_from_user_not_registered(from_user_id):
    pass


@task
def send_bad_balance(from_user_id):
    pass
