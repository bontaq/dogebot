from django.conf import settings
import json
import requests
import logging
from decimal import Decimal
from core.models import WalletTransaction

logger = logging.getLogger()
MIN_CONFIRMATIONS = 3


class InvalidAddress(Exception):
    pass


class WalletAPI():
    def __init__(self):
        self.client = requests.Session()
        self.client.auth = ('dogecoinrpc', settings.WALLET_AUTH)
        self.base_url = settings.WALLET_LOCATION
        self.rpc_id = 0

    def wallet_request(self, method, *args):
        """Handler for all requests, sends it straight to the rpc"""

        data = {
            "jsonrpc": "1.0",
            "id": self.rpc_id,
            "method": method,
            "params": args,
        }
        results = self.client.get(
            self.base_url,
            data=json.dumps(data)
        )
        self.rpc_id += 1
        return results.json()['result']

    def validate_address(self, address):
        """Returns if an address is valid or not"""

        result = self.wallet_request("validateaddress", *[address])
        return result['isvalid']

    def wallet_amount(self):
        """Total amount of doge in the wallet"""

        results = self.wallet_request("listunspent")
        return sum(result['amount'] for result in results)

    def amount_received(self, address):
        """Returns amount received by an address"""

        return self.wallet_request("getreceivedbyaddress", *[address])

    def send_amount(self, address, amount, from_wallet="users"):
        """Send doge to a foreign address.  If the address is invalid, will raise InvalidAddress"""

        if self.validate_address(address):
            txid = self.wallet_request("sendfrom", *[from_wallet, address, (float(amount) + 1)])
            logger.info('Sent %s to %s', amount, address)
            return txid
        else:
            raise InvalidAddress(address)

    def get_new_address(self):
        """Returns a new address in the users wallet"""

        address = self.wallet_request("getnewaddress", *["users"])
        logger.info('created wallet address: %s', address)
        return address

    def get_new_deposits(self, last_transaction=None):
        """Looks for new deposits in the list of transaction and returns them

        :param last_transaction: WalletTransaction
        :returns: [WalletTransaction]
        """
        offset = 0
        new_deposits = []
        while True:
            transactions = self.wallet_request("listtransactions", *["users", 10, offset])
            transactions.reverse()
            if transactions:
                for trans in [t for t in transactions
                              if t["category"] in ["receive", "send"]
                              and t["confirmations"] >= MIN_CONFIRMATIONS]:
                    if last_transaction and last_transaction.txid == trans["txid"]:
                        return new_deposits
                    elif trans["category"] == "receive":
                        new_deposits.append(WalletTransaction(
                            to_address=trans["address"],
                            is_deposit=True,
                            amount=Decimal(trans["amount"]),
                            confirmations=trans["confirmations"],
                            txid=trans["txid"]
                        ))
                offset += 10
            else:
                return new_deposits
