# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('convo_id', models.CharField(max_length=128)),
                ('user_name', models.CharField(max_length=128, null=True)),
                ('user_id', models.CharField(max_length=24, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('needs_update', models.BooleanField(default=True)),
                ('last_message_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.CharField(max_length=128)),
                ('processed', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=512, null=True)),
                ('user_name', models.CharField(max_length=128, null=True)),
                ('user_id', models.CharField(max_length=24, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.CharField(max_length=128, null=True)),
                ('user_id', models.CharField(max_length=24, null=True)),
                ('sent_at', models.DateTimeField()),
                ('processed', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=512)),
                ('conversation', models.ForeignKey(to='core.Conversation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('pending', models.BooleanField(default=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=128, db_index=True)),
                ('user_id', models.CharField(max_length=24, null=True)),
                ('balance', models.FloatField(default=0, null=True)),
                ('deposit_address', models.CharField(max_length=34)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_deposit', models.BooleanField(default=False)),
                ('is_withdrawl', models.BooleanField(default=False)),
                ('to_address', models.CharField(max_length=34)),
                ('amount', models.FloatField()),
                ('pending', models.BooleanField(default=True)),
                ('confirmations', models.IntegerField(default=0)),
                ('txid', models.CharField(max_length=64)),
                ('user', models.ForeignKey(to='core.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='from_user',
            field=models.ForeignKey(related_name='transaction_from_users', to='core.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='to_user',
            field=models.ForeignKey(related_name='transaction_to_users', to='core.User'),
            preserve_default=True,
        ),
    ]
