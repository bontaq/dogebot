from django.conf import settings
from datetime import datetime
import pytz
import logging
from decimal import Decimal
from core.models import Message, User, Transaction, Mention, WalletTransaction, StuckMessage
from core.soundcloud_api import SoundCloudAPI
import core.soundcloud_parses as SCParser
from core.wallet import WalletAPI, InvalidAddress
from core import tasks

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

    def handle_created_user(self, user, created, text):
        """Welcomes user or lets them know they've already registed"""

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

    def handle_withdrawl(self, amt, address, user):
        """Transfers funds to an outside address"""

        if amt == 'all' or user.balance >= amt:
            amt_to_send = user.balance if amt == 'all' else amt
            result = self.wallet.send_amount(address, amt_to_send)
            if result:
                user.balance -= amt_to_send
                user.save()
                wallet_transaction = WalletTransaction(
                    user=user,
                    is_withdrawl=True,
                    amount=amt_to_send,
                    txid=result,
                    to_address=address
                )
                wallet_transaction.save()
                tasks.send_successful_withdrawl.delay(user, amt_to_send, address)
                logger.info(wallet_transaction)
        else:
            raise BadBalance()

    def process_messages(self):
        """Everything to do with messages: registery, get_balance, withdrawl, and history"""

        for message in Message.objects.filter(processed=False):
            text = message.message
            if SCParser.is_register(text) or SCParser.is_accept(text):
                user, created = self.register_user(message)
                self.handle_created_user(user, created, text)
                message.processed = True
                message.save()
            elif SCParser.is_get_balance(text):
                user = User.objects.get(user_id=message.user_id)
                try:
                    tasks.send_balance.delay(user)
                    message.processed = True
                    message.save()
                except Exception as e:
                    logger.exception(e)
            elif SCParser.is_withdrawl(text):
                amt, address = SCParser.parse_withdrawl(text)
                try:
                    user = User.objects.get(user_id=message.user_id)
                    self.handle_withdrawl(amt, address, user)
                except InvalidAddress:
                    tasks.send_invalid_address.delay(user, address)
                except BadBalance:
                    tasks.send_bad_balance_withdrawl.delay(user, amt)
                except User.DoesNotExist:
                    tasks.send_unregistered_withdrawl.delay(message.user_id)
                message.processed = True
                message.save()
            elif SCParser.is_history(text):
                user = User.objects.get(user_id=message.user_id)
                tasks.send_history.delay(user)
                message.processed = True
                message.save()
            elif SCParser.is_help(text):
                tasks.send_help.delay(message.user_id)
                message.processed = True
                message.save()

    def is_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()

    def transfer_funds(self, from_user, to_user, amt):
        """Transfer funds between users in the network

        :param from_user: User
        :param to_user: User
        :param amt: Decimal
        """
        from_user.balance -= amt
        from_user.save()
        # because some oddballs like to tip themselves
        to_user = User.objects.get(id=to_user.id)
        to_user.balance += amt
        to_user.save()
        trans = Transaction(
            from_user=from_user,
            to_user=to_user,
            amount=amt,
            pending=False,
            accepted=True
        )
        trans.save()
        logger.info('Moved coin: %s', trans)
        return trans

    def handle_to_user_not_registered(self, from_user_id, to_user_id, amt):
        """Creates pending transaction and subtracts tip amount from from_user"""

        from_user = User.objects.get(user_id=from_user_id)
        if from_user.balance >= amt:
            trans = Transaction(
                from_user=User.objects.get(user_id=from_user_id),
                to_user_temp_id=to_user_id,
                amount=amt,
                pending=True,
                accepted=False,
            )
            trans.save()
            logger.info('Created pending transaction: %s', trans)
            from_user.balance -= amt
            from_user.save()
        else:
            raise BadBalance()

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
                    tasks.send_from_user_not_registered.delay(from_user_id)
                except ToUserNotRegistered:
                    try:
                        self.handle_to_user_not_registered(from_user_id, to_user_id, amt_to_send)
                        tasks.send_notify_from_user_pending_tip.delay(from_user_id, to_user_id, amt_to_send)
                        tasks.send_notify_of_tip.delay(from_user_id, to_user_id)
                    except BadBalance:
                        tasks.send_bad_balance.delay(from_user_id, to_user_id, amt_to_send)
                except BadBalance:
                    tasks.send_bad_balance.delay(from_user_id, to_user_id, amt_to_send)
            mention.processed = True
            mention.save()

    def process_tip(self, from_user_id, to_user_id, amt):
        """Handles a mention-based tip, from_user to_user"""

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
        """Go through pending transactions and see if the recipient has accepted, then complete transaction.
        If the request is over 3 days old return funds and inform the tipper."""

        now = datetime.now(pytz.utc)
        for transaction in Transaction.objects.filter(pending=True):
            if (now - transaction.timestamp).total_seconds() > settings.TIP_EXPIRY:
                transaction.from_user.balance += transaction.amount
                transaction.pending = False
                transaction.from_user.save()
                transaction.save()
                logger.info('Refunded pending tip, from_user: %s, to_user: %s, amt: %s',
                            transaction.from_user.user_id,
                            transaction.to_user_temp_id,
                            transaction.amount.quantize(Decimal('0.00')))
                tasks.send_notify_of_refund.delay(transaction.from_user,
                                                  transaction.to_user_temp_id,
                                                  transaction.amount)
            else:
                try:
                    to_user = User.objects.get(user_id=transaction.to_user_temp_id)
                    to_user.balance += transaction.amount
                    to_user.save()
                    transaction.to_user = to_user
                    transaction.pending = False
                    transaction.accepted = True
                    transaction.save()
                    logger.info('Completed pending tip, from_user: %s, to_user: %s, amt: %s',
                                transaction.from_user.user_id,
                                to_user.user_id,
                                transaction.amount.quantize(Decimal('0.00')))
                    tasks.send_tip_success.delay(transaction.from_user.user_id, to_user.user_id, transaction.amount)
                except User.DoesNotExist:
                    pass

    def process_deposits(self):
        """Check for latest deposits and credits user account"""

        try:
            last_transaction = WalletTransaction.objects.latest('timestamp')
        except WalletTransaction.DoesNotExist:
            last_transaction = None

        new_deposits = self.wallet.get_new_deposits(last_transaction)
        for deposit in new_deposits:
            if WalletTransaction.objects.filter(txid=deposit.txid).exists():
                logger.warning('Tried to recreate a deposit, %s', deposit)
            else:
                try:
                    user = User.objects.get(deposit_address=deposit.to_address)
                    user.balance += deposit.amount
                    user.save()
                    deposit.user = user
                    deposit.pending = False
                    deposit.save()
                    tasks.send_successful_deposit.delay(user, deposit)
                except User.DoesNotExist:
                    logger.error('User could not be found for deposit to %s', deposit.to_address)

    def clear_stuck_messages(self):
        for m in StuckMessage.objects.all():
            self.soundcloud.send_message(to_user_id=m.user_id, message=m.message)
            # if the message fails again, another StuckMessage will be created, so always
            # delete the old one.
            m.delete()
