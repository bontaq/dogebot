from core.models import Message, User, Transaction, Mention
from core.soundcloud_api import SoundCloudAPI
import core.soundcloud_parses as SCParser
from core.wallet import WalletAPI
from core import tasks
import logging

logger = logging.getLogger(__name__)


class FromUserNotRegistered(Exception):
    pass


class ToUserNotRegistered(Exception):
    pass


class BadBalance(Exception):
    pass


class Processor():
    def __init__(self):
        self.wallet = WalletAPI()
        self.soundcloud = SoundCloudAPI()

    def register_user(self, message):
        """Try to create a User with a deposit address, returns a User and created if it was
        successful"""
        user, created = User.objects.get_or_create(
            user_name=message.user_name,
            user_id=message.user_id,
        )
        if created:
            user.deposit_address = self.wallet.get_new_address()
            user.save()
        return user, created

    def process_messages(self):
        for message in Message.objects.filter(processed=False):
            text = message.message
            if SCParser.is_register(text):
                user, created = self.register_user(message)
                if created:
                    tasks.send_welcome.delay(user)
                    logger.info('user created, username: %s, id: %s, message: %s',
                                user.user_name,
                                user.user_id,
                                text)
                else:
                    tasks.send_already_registered.delay(user)
                    logger.info('user tried to reregister, username: %s, id: %s, message: %s',
                                user.user_name,
                                user.user_id,
                                text)
                message.processed = True
                message.save()
            elif SCParser.is_get_balance(text):
                user = User.objects.get(user_id=message.user_id)
                try:
                    tasks.send_balance(user)
                    message.processed = True
                    message.save()
                except Exception as e:
                    logger.exception(e)
            # withdraw
            # history

    def is_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()

    def transfer_funds(self, from_user, to_user, amt):
        """
        :param from_user: User
        :param to_user: User
        :param amt: int or float
        """
        from_user.balance -= amt
        to_user.balance += amt
        from_user.save()
        to_user.save()
        trans = Transaction(
            from_user=from_user,
            to_user=to_user,
            amount=amt,
            pending=False,
            accepted=True
        )
        trans.save()
        return trans

    def process_mentions(self):
        """Goes through unprocessed mentions and manages those which are tips"""
        for mention in Mention.objects.filter(processed=False):
            if SCParser.is_mention_tip(mention.message):
                from_user_id = mention.from_user_id
                to_user_id = mention.to_user_id
                amt_to_send = SCParser.parse_mention_tip(mention.message)
                try:
                    self.process_tip(from_user_id, to_user_id, amt_to_send)
                    tasks.send_tip_success.delay(from_user_id, to_user_id, amt_to_send)
                except FromUserNotRegistered:
                    tasks.send_from_user_not_registered(from_user_id)
                except ToUserNotRegistered:
                    Transaction(
                        from_user=from_user_id,
                        to_user=to_user_id,
                        amount=amt_to_send,
                        pending=True,
                        accepted=False
                    ).save()
                    tasks.send_notify_from_user_pending_tip(from_user_id, to_user_id, amt)
                    tasks.send_notify_of_tip(from_user_id, to_user_id)
                except BadBalance:
                    tasks.send_bad_balance(from_user_id)
            mention.processed = True
            mention.save()

    def process_tip(self, from_user_id, to_user_id, amt):
        try:
            from_user = User.objects.get(user_id=from_user_id)
        except User.DoesNotExist:
            raise FromUserNotRegistered()

        try:
            to_user = User.objects.get(user_id=to_user_id)
        except User.DoesNotExist:
            raise ToUserNotRegistered()

        if from_user.balance < amt:
            raise BadBalance()

        self.transfer_funds(from_user, to_user, amt)

    def process_transactions(self):
        pass
