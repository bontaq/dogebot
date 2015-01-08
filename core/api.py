from tastypie.resources import ModelResource, fields
from core.models import Message, WalletTransaction, Transaction, User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        allowed_methods = ['get']


class WalletResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = WalletTransaction.objects.all()
        resource_name = 'wallettransaction'
        allowed_methods = ['get']


class TransactionResource(ModelResource):
    from_user = fields.ToOneField(UserResource, 'from_user', full=True)
    to_user = fields.ToOneField(UserResource, 'to_user', full=True)

    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'
        allowed_methods = ['get']
