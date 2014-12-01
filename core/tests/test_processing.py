from datetime import datetime
from django.test import TestCase
from mock import patch
from django_dynamic_fixture import G
from core.processing import (Processor, BadBalance, FromUserNotRegistered,
                             ToUserNotRegistered)
from core.models import Conversation, Message, User, Transaction, Mention
from decimal import Decimal


class ProcessTests(TestCase):
    @patch('core.processing.SoundCloudAPI')
    @patch('core.processing.WalletAPI')
    def setUp(self, mock_wallet, mock_soundcloud):
        self.mock_wallet = mock_wallet
        self.mock_soundcloud = mock_soundcloud
        self.processor = Processor()

    @patch('core.tasks')
    def test_register_response(self, mock_tasks):
        self.mock_wallet.return_value.get_new_address.return_value = '1'
        convo = Conversation(
            convo_id='test',
            last_message_time=datetime.now()
        )
        convo.save()
        Message(
            user_name='bopeep2',
            user_id='whatev',
            conversation=convo,
            message='register',
            sent_at=datetime.now()
        ).save()
        self.processor.process_messages()
        self.assertEqual(User.objects.get(user_name='bopeep2').deposit_address, '1')

    @patch('core.tasks')
    def test_register_user_already_exists(self, mock_tasks):
        u = G(User)
        c = G(Conversation)
        m = Message(
            user_name=u.user_name,
            user_id=u.user_id,
            conversation=c,
            message='register',
            sent_at=datetime.now()
        )
        user, created = self.processor.register_user(m)
        self.assertFalse(created)

    @patch('core.tasks.send_balance')
    def test_send_balance(self, mock_send_balance):
        u = G(User)
        m = G(Message, message='balance', user_id=u.user_id, processed=False)
        self.processor.process_messages()
        self.assertTrue(mock_send_balance.called)
        m_updated = Message.objects.get(pk=m.id)
        self.assertTrue(m_updated.processed)

    def test_transfer_funds_user_amount(self):
        user_a = G(User)
        user_b = G(User)
        self.processor.transfer_funds(user_a, user_b, 50)
        user_a_after = User.objects.get(id=user_a.id)
        user_b_after = User.objects.get(id=user_b.id)
        self.assertEqual(user_a_after.balance, -50)
        self.assertEqual(user_b_after.balance, 50)

    def test_transfer_funds_transaction_creation(self):
        user_a = G(User)
        user_b = G(User)
        returned_trans = self.processor.transfer_funds(user_a, user_b, 50)
        trans = Transaction.objects.get(id=returned_trans.id)
        self.assertIsNotNone(trans)
        self.assertEqual(trans.amount, 50)
        self.assertFalse(trans.pending)
        self.assertTrue(trans.accepted)

    def test_process_mention_both_users_registered(self):
        user_a = G(User, balance=Decimal(500))
        user_b = G(User, balance=Decimal(0))
        mention = G(
            Mention,
            processed=False,
            message='@dogebot tip 100',
            from_user_id=user_a.user_id,
            to_user_id=user_b.user_id
        )
        self.processor.process_mentions()
        user_a_after = User.objects.get(user_id=user_a.user_id)
        user_b_after = User.objects.get(user_id=user_b.user_id)
        self.assertEqual(user_a_after.balance, 400)
        self.assertEqual(user_b_after.balance, 100)
        mention_after = Mention.objects.get(id=mention.id)
        self.assertTrue(mention_after.processed)

    def test_proccess_mention_pending_transaction(self):
        pass

    def test_process_tip_not_enough_balance(self):
        user_a = G(User, balance=Decimal(100))
        user_b = G(User, balance=Decimal(0))
        with self.assertRaises(BadBalance):
            self.processor.process_tip(user_a.user_id, user_b.user_id, Decimal(500))

    def test_process_tip_from_user_unregistered(self):
        user_b = G(User, balance=Decimal(0))
        with self.assertRaises(FromUserNotRegistered):
            self.processor.process_tip('Z', user_b.user_id, Decimal(500))

    def test_process_tip_to_user_unregistered(self):
        user_a = G(User, balance=Decimal(100))
        with self.assertRaises(ToUserNotRegistered):
            self.processor.process_tip(user_a.user_id, 'Z', Decimal(500))
