from tastypie.resources import ModelResource, fields
from core.models import Message, WalletTransaction, Transaction, User, Mention


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all().order_by('timestamp')
        resource_name = 'message'
        allowed_methods = ['get']


class MentionResource(ModelResource):
    class Meta:
        queryset = Mention.objects.all().order_by('timestamp')
        resource_name = 'mention'
        allowed_methods = ['get']


class WalletResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = WalletTransaction.objects.all().order_by('timestamp')
        resource_name = 'wallettransaction'
        allowed_methods = ['get']


class TransactionResource(ModelResource):
    from_user = fields.ToOneField(UserResource, 'from_user', full=True)
    to_user = fields.ToOneField(UserResource, 'to_user', full=True, null=True)

    class Meta:
        queryset = Transaction.objects.all().order_by('timestamp')
        resource_name = 'transaction'
        allowed_methods = ['get']
