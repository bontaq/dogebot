from core.wallet import WalletAPI
from django.test import TestCase


class WalletAPITests(TestCase):
    def setUp(self):
        self.wallet = WalletAPI()

    def test_wallet_amount(self):
        result = self.wallet.wallet_amount()
        self.assertTrue(result > 0)

    def test_validate_address(self):
        result = self.wallet.validate_address("DQvhVFe1tcSmkRKKWjuhtDePSk7k47b4Vc")
        self.assertTrue(result)

    def test_get_received_by(self):
        result = self.wallet.amount_received(address="DQvhVFe1tcSmkRKKWjuhtDePSk7k47b4Vc")
        self.assertTrue(result > 0)

    def test_send_amount(self):
        result = self.wallet.send_amount("DQNGcuNArnAsmYhJCsg6tdRCGNUpgSWPTr", 10)

    def test_create_new_address(self):
        result = self.wallet.get_new_address()
        self.assertIsNotNone(result)
