from django.conf import settings
import json
import requests
import logging
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
        result = self.wallet_request("validateaddress", *[address])
        return result['isvalid']

    def wallet_amount(self):
        results = self.wallet_request("listunspent")
        return sum(result['amount'] for result in results)

    def amount_received(self, address):
        return self.wallet_request("getreceivedbyaddress", *[address])

    def send_amount(self, address, amount, from_wallet="users"):
        if self.validate_address(address):
            return self.wallet_request("sendfrom", *[from_wallet, address, amount])
        else:
            raise InvalidAddress(address)

    def get_new_address(self):
        address = self.wallet_request("getnewaddress", *["users"])
        logger.info('created wallet address: %s', address)
        return address

    def get_new_deposits(self, last_deposit=None):
        """
        :param last_deposit: WalletTransaction
        :returns: [WalletTransaction]
        """
        offset = 0
        new_deposits = []
        while True:
            transactions = self.wallet_request("listtransactions", *["users", 10, offset])
            if transactions:
                for trans in [t for t in transactions
                              if t["category"] == "receive"
                              and t["confirmations"] >= MIN_CONFIRMATIONS]:
                    if last_deposit and last_deposit.txid == trans["txid"]:
                        return new_deposits
                    else:
                        new_deposits.append(WalletTransaction(
                            to_address=trans["address"],
                            is_deposit=True,
                            amount=trans["amount"],
                            confirmations=trans["confirmations"],
                            txid=trans["txid"]
                        ))
                offset += 10
            else:
                return new_deposits
