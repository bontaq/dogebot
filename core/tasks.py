from celery import task
from core.soundcloud_api import SoundCloudAPI
from core.models import User
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


@task
def send_welcome(user):
    soundcloud = SoundCloudAPI()
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
    soundcloud = SoundCloudAPI()
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
    soundcloud = SoundCloudAPI()
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
    soundcloud = SoundCloudAPI()
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
def send_notify_of_tip(from_user_id, to_user_id):
    soundcloud = SoundCloudAPI()
    from_user = soundcloud.get_soundcloud_user(user_id=from_user_id)
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = "{from_user} would like to send you a dogecoin tip, reply with 'accept' to " \
          "register and accept this tip.".format(
              from_user=from_user['username']
          )
    try:
        soundcloud.send_message(to_user['id'], msg)
        logger.info('Reply: asked user to register.  from_user: %s, to_user: %s',
                    from_user,
                    to_user)
    except Exception as e:
        logger.exception(e)


@task
def send_notify_from_user_pending_tip(from_user_id, to_user_id, amt):
    soundcloud = SoundCloudAPI()
    from_user = soundcloud.get_soundcloud_user(user_id=from_user_id)
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = ("You sent {to_user} a tip of {amt}, they aren't current registered but I'll "
           "let you know if they accept the tip.").format(
               to_user=to_user['username'],
               amt=amt.quantize(Decimal("0.00")))
    try:
        soundcloud.send_message(to_user['id'], msg)
    except Exception as e:
        logger.exception(e)


@task
def send_from_user_tip_refunded(from_user, to_user_id, amt):
    soundcloud = SoundCloudAPI()
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = ("You tried to tip {to_user}, but they did not accept in time.  "
           "{amt} doge has been refunded to you").format(
               to_user=to_user['username'],
               amt=amt.quantize(Decimal('0.00')))
    try:
        soundcloud.send_message(to_user['id'], msg)
    except Exception as e:
        logger.exception(e)


@task
def send_from_user_not_registered(from_user_id):
    soundcloud = SoundCloudAPI()
    msg = ("You tried to tip someone but have not registered.  Respond with "
           "'register' if you would like to register.")
    try:
        soundcloud.send_message(to_user['id'], msg)
        logger.info('Notified %s that they are not registered', from_user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_bad_balance(from_user_id, to_user_id, amt):
    soundcloud = SoundCloudAPI()
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    from_user = User.objects.get(user_id=from_user_id)
    msg = ("You tried to send a tip of {amt} doges to {user}, but your balance is {balance} doges").format(
        amt=amt.quantize(Decimal("0.00")),
        user=to_user['username'],
        balance=from_user.balance.quantize(Decimal("0.00"))
    )
    try:
        soundcloud.send_message(from_user_id, msg)
        logger.info('Notified %s that they do not have sufficient balance', from_user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_notify_of_refund(from_user, to_user_id, amt):
    soundcloud = SoundCloudAPI()
    to_user = soundcloud.get_soundcloud_user(user_id=to_user_id)
    msg = ("The tip you tried to send to {to_user} of {amt} doges "
           "has been refunded to you").format(
               to_user=to_user['username'],
               amt=amt.quantize(Decimal("0.00")))
    try:
        soundcloud.send_message(from_user.user_id, msg)
        logger.info('Notified %s of refund to %s', from_user.user_id, to_user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_successful_deposit(user, deposit):
    soundcloud = SoundCloudAPI()
    msg = ("Your deposit of {amt} doges was recieved. \n"
           "Your balance is now {balance} doges.").format(
               amt=deposit.amount,
               balance=user.balance)
    try:
        soundcloud.send_message(user.user_id, msg)

        logger.info('Notified %s of deposit', user.user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_invalid_address(user, address):
    soundcloud = SoundCloudAPI()
    msg = ("The address you tried to send doge to was invalid.\n"
           "address recieved: {addr}".format(
               addr=address
           ))
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Notified %s of invalid address', user.user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_bad_balance_withdrawl(user, amt):
    soundcloud = SoundCloudAPI()
    msg = ("You tried to withdraw {amt}, but your balance is only {balance}".format(
        amt=amt.quantize(Decimal("0.00")),
        balance=user.balance.quantize(Decimal("0.00"))
    ))
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Notified %s of insufficient funds address', user.user_id)
    except Exception as e:
        logger.exception(e)


@task
def send_successful_withdrawl(user, amt, address):
    soundcloud = SoundCloudAPI()
    msg = ("Successfully withdrew {amt} doges.\n"
           "Sent to: {addr}"
           "New balance: {balance}").format(
               amt=amt.quantize(Decimal("0.00")),
               addr=address,
               balance=user.balance.quantize(Decimal("0.00")))
    try:
        soundcloud.send_message(user.user_id, msg)
        logger.info('Notified %s of insufficient funds address', user.user_id)
    except Exception as e:
        logger.exception(e)
