from django.conf import settings
import json
import requests
import logging

logger = logging.getLogger()


class WalletAPI():
    def __init__(self):
        self.client = requests.Session()
        self.client.auth = ('dogecoinrpc', settings.WALLET_AUTH)
        self.base_url = settings.WALLET_LOCATION

    def wallet_request(self, method, *args):
        data = {
            "jsonrpc": "1.0",
            "id": "1",
            "method": method,
            "params": args,
        }
        results = self.client.get(
            self.base_url,
            data=json.dumps(data)
        )
        return results.json()['result']

    def validate_address(self, address):
        result = self.wallet_request("validateaddress", *[address])
        return result['isvalid']

    def wallet_amount(self):
        results = self.wallet_request("listunspent")
        return sum(result['amount'] for result in results)

    def amount_received(self, address):
        return self.wallet_request("getreceivedbyaddress", *[address])

    def send_amount(self, address, amount):
        if self.validate_address(address):
            result = self.wallet_request("sendtoaddress", *[address, amount])
        return result

    def get_new_address(self):
        address = self.wallet_request("getnewaddress")
        logger.info('created wallet address: %s', address)
        return address

    def create_withdrawls(self):
        pass

    # def update_transactions_status(self):
    #     # go through unprocessed wallet transactions, created by parser, and process them
    #     for transaction in WalletTransaction.objects.filter(pending=True):
    #         pass

    # def update_transactions(self):
    #     pass
