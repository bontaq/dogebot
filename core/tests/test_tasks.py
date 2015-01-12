from django_dynamic_fixture import G
from mock import patch
from django.test import TestCase
from core.models import WalletTransaction, Transaction, User
from core import tasks
from datetime import datetime, timedelta
from decimal import Decimal
from django.test.utils import override_settings


@override_settings(BROKER_BACKEND='memory',
                   CELERY_ALWAYS_EAGER=True,
                   CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestTasks(TestCase):
    @patch('core.tasks.SoundCloudAPI.send_message')
    def test_history_task(self, mock_message):
        user_a = G(User, user_name='TestUser')
        user_b = G(User, user_name='OtherUser')
        now = datetime.now()
        G(Transaction,
          from_user=user_a,
          to_user=user_b,
          timestamp=now - timedelta(seconds=10),
          amount=100)
        G(Transaction,
          from_user=user_b,
          to_user=user_a,
          amount=50)
        G(WalletTransaction, user=user_a, is_withdrawl=True,
          timestamp=now - timedelta(seconds=5), amount=200)
        tasks.send_history(user_a)
        mock_message.assert_called_with(
            str(user_a.user_id),
            ("Here is a history of your transactions: \n"
             "Received from OtherUser 50.00 doges \n"
             "Withdrew 200.00 doges \nTipped OtherUser 100.00 doges \n")
        )

    def test_history_tipped(self):
        user = G(User, user_name="receiver")
        tipper = G(User, user_name="tipper")
        G(Transaction,
          from_user=tipper,
          to_user=user,
          amount=Decimal(10))
        result = tasks.build_history(user)
        self.assertEqual(result, "Received from tipper 10.00 doges \n")

    def test_history_tip_recieved(self):
        user = G(User, user_name="Tipper")
        receiver = G(User, user_name="receiver")
        G(Transaction,
          from_user=user,
          to_user=receiver,
          amount=Decimal(10))
        result = tasks.build_history(user)
        self.assertEqual(result, "Tipped receiver 10.00 doges \n")

    def test_history_withdraw(self):
        user = G(User)
        G(WalletTransaction,
          user=user,
          is_withdrawl=True,
          is_deposit=False,
          amount=Decimal(100))
        result = tasks.build_history(user)
        self.assertEqual(result, "Withdrew 100.00 doges \n")

    def test_history_deposit(self):
        user = G(User)
        G(WalletTransaction,
          user=user,
          is_withdrawl=False,
          is_deposit=True,
          amount=Decimal(100))
        result = tasks.build_history(user)
        self.assertEqual(result, "Deposited 100.00 doges \n")
