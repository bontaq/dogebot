from tastypie.resources import ModelResource
from core.models import Message, WalletTransaction, Transaction, User


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        allowed_methods = ['get']


class WalletResource(ModelResource):
    class Meta:
        queryset = WalletTransaction.objects.all()
        resource_name = 'wallettransaction'
        allowed_methods = ['get']


class TransactionResource(ModelResource):
    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'
        allowed_methods = ['get']


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']
