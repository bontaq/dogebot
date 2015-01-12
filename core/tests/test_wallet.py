from mock import patch
from django.test import TestCase
from django_dynamic_fixture import G
from core.models import WalletTransaction
from core.tests.fixture import wallet_transactions_fixture
from core.wallet import WalletAPI, InvalidAddress


class WalletAPITests(TestCase):
    def setUp(self):
        self.wallet = WalletAPI()

    def test_wallet_amount(self):
        result = self.wallet.wallet_amount()
        self.assertTrue(result > 0)

    @patch('core.wallet.WalletAPI.wallet_request')
    def test_validate_address(self, mock_request):
        self.wallet.validate_address("DQvhVFe1tcSmkRKKWjuhtDePSk7k47b4Vc")
        mock_request.assert_called_with('validateaddress', 'DQvhVFe1tcSmkRKKWjuhtDePSk7k47b4Vc')

    @patch('core.wallet.WalletAPI.wallet_request')
    def test_get_received_by(self, mock_request):
        mock_request.return_value = 100.0
        result = self.wallet.amount_received(address="DQvhVFe1tcSmkRKKWjuhtDePSk7k47b4Vc")
        self.assertTrue(result > 0)

    @patch('core.wallet.WalletAPI.validate_address')
    @patch('core.wallet.WalletAPI.wallet_request')
    def test_send_amount(self, mock_request, mock_validate):
        txid = u'6cb18a509482d16595a8c2de0fd31d630e3f5f472f7d297e660576380ae918f7'
        mock_request.return_value = txid
        mock_validate.return_value = True
        result = self.wallet.send_amount("DQNGcuNArnAsmYhJCsg6tdRCGNUpgSWPTr", 10)
        self.assertEqual(result, txid)

    @patch('core.wallet.WalletAPI.validate_address')
    @patch('core.wallet.WalletAPI.wallet_request')
    def test_bad_send_amount(self, mock_request, mock_validate):
        txid = u'6cb18a509482d16595a8c2de0fd31d630e3f5f472f7d297e660576380ae918f7'
        mock_request.return_value = txid
        mock_validate.return_value = False
        with self.assertRaises(InvalidAddress):
            result = self.wallet.send_amount("DQNGcuNArnAsmYhJCsg6tdRCGNUpgSWPTr", 10)

    @patch('core.wallet.WalletAPI.wallet_request')
    def test_create_new_address(self, mock_request):
        mock_request.return_value = 'NotNone!'
        result = self.wallet.get_new_address()
        self.assertIsNotNone(result)

    @patch('core.wallet.WalletAPI.wallet_request')
    def test_get_new_deposits(self, mock_wallet):
        mock_wallet.side_effect = [wallet_transactions_fixture, []]
        results = self.wallet.get_new_deposits()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].amount, 100)
        self.assertEqual(results[0].to_address, "nfcs52piVXTkvVwBu7L3FGzV663mapMSao")
        self.assertEqual(results[0].txid, "bafe23fc47d4d5b4e9f188264c8de4e82e5134be1a93d6053f5010a58b85d65d")
        self.assertTrue(results[0].is_deposit)

    @patch('core.wallet.WalletAPI.wallet_request')
    def test_no_new_deposits(self, mock_wallet):
        transaction = G(WalletTransaction, txid="bafe23fc47d4d5b4e9f188264c8de4e82e5134be1a93d6053f5010a58b85d65d")
        mock_wallet.side_effect = [wallet_transactions_fixture, []]
        results = self.wallet.get_new_deposits(transaction)
        self.assertEqual(results, [])
