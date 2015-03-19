from django.db import models

"""
As a general note, do not trust user_name fields.  The soundcloud user can change that.
Instead rely on the user_id fields.
"""


class Mention(models.Model):
    timestamp = models.DateTimeField()
    uuid = models.CharField(max_length=128, unique=True)
    processed = models.BooleanField(default=False)
    message = models.CharField(max_length=512, null=True)
    from_user_name = models.CharField(max_length=128, null=True)
    from_user_id = models.CharField(max_length=24, null=True)
    to_user_name = models.CharField(max_length=128, null=True)
    to_user_id = models.CharField(max_length=24, null=True)
    on_track_url = models.TextField()

    def __str__(self):
        return "{time}, {uuid}, {message}, {from_user}, {to_user}".format(
            time=self.timestamp,
            uuid=self.uuid,
            message=self.message,
            from_user=self.from_user_name,
            to_user=self.to_user_name
        )


class Conversation(models.Model):
    convo_id = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128, null=True)
    user_id = models.CharField(max_length=24, null=True)
    processed = models.BooleanField(default=False)
    needs_update = models.BooleanField(default=True)
    last_message_time = models.DateTimeField()

    def __str__(self):
        return "{convo_id}, {user_name}, {user_id}, {processed}, {last_message_time}".format(
            convo_id=self.convo_id,
            user_name=self.user_name,
            user_id=self.user_id,
            processed=self.processed,
            last_message_time=self.last_message_time
        )


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=128, null=True)
    user_id = models.CharField(max_length=24, null=True)
    sent_at = models.DateTimeField()
    conversation = models.ForeignKey(Conversation)
    processed = models.BooleanField(default=False)
    message = models.TextField(null=True)

    def __str__(self):
        return "{timestamp}, {user_name}, {user_id}, {message}".format(
            timestamp=self.timestamp,
            user_name=self.user_name,
            user_id=self.user_id,
            message=self.message
        )


class StuckMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=24)
    message = models.TextField()
    error = models.TextField()

    def __str__(self):
        return "{timestamp}, {user_id}, {message}".format(
            timestamp=self.timestamp,
            user_id=self.user_id,
            message=self.message
        )


class User(models.Model):
    user_name = models.CharField(db_index=True, max_length=128)
    user_id = models.CharField(max_length=24, unique=True)
    balance = models.DecimalField(null=True, default=0, max_digits=50, decimal_places=8)
    deposit_address = models.CharField(max_length=40, null=True)

    def __str__(self):
        return "{user_name}, {user_id}, {balance}, {deposit_address}".format(
            user_name=self.user_name,
            user_id=self.user_id,
            balance=self.balance,
            deposit_address=self.deposit_address
        )


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, related_name='transaction_from_users')
    to_user = models.ForeignKey(User, related_name='transaction_to_users', null=True)
    to_user_temp_id = models.CharField(max_length=24, null=True)  # used for when the to_user is not registered
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    parent_transaction = models.ForeignKey('Transaction', null=True)

    def __str__(self):
        return "{timestamp}, from:{from_user}, to:{to_user}, {amt}".format(
            timestamp=self.timestamp,
            from_user=self.from_user.user_id,
            to_user=self.to_user.user_id if self.to_user else self.to_user_temp_id,
            amt=self.amount
        )


class WalletTransaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    is_deposit = models.BooleanField(default=False)
    is_withdrawl = models.BooleanField(default=False)
    to_address = models.CharField(max_length=34)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    pending = models.BooleanField(default=True)
    confirmations = models.IntegerField(default=0)
    txid = models.CharField(max_length=64)

    def __str__(self):
        return ("{time}, u:{user}, deposit:{deposit}, withdrawl:{withdrawl}, "
                "amt:{amount}, pending:{pending}, confs:{confirmations}, "
                "txid:{txid}").format(
                    time=self.timestamp,
                    user=self.user.user_id if self.user else "None",
                    deposit=self.is_deposit,
                    withdrawl=self.is_withdrawl,
                    amount=self.amount,
                    pending=self.pending,
                    confirmations=self.confirmations,
                    txid=self.txid
                )
