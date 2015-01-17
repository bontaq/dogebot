# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'core', '0001_initial'), (b'core', '0002_auto_20141102_2341'), (b'core', '0003_auto_20141105_2142'), (b'core', '0004_auto_20141113_1831'), (b'core', '0005_auto_20141113_1841'), (b'core', '0006_auto_20141113_2225'), (b'core', '0007_auto_20141113_2229'), (b'core', '0008_auto_20141118_0006'), (b'core', '0009_auto_20141129_1647'), (b'core', '0010_auto_20141129_1924'), (b'core', '0011_auto_20141204_1417'), (b'core', '0012_transaction_parent_transaction'), (b'core', '0013_transaction_closed'), (b'core', '0014_remove_transaction_closed'), (b'core', '0015_auto_20141215_0958')]

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
                ('timestamp', models.DateTimeField()),
                ('uuid', models.CharField(unique=True, max_length=128)),
                ('processed', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=512, null=True)),
                ('from_user_name', models.CharField(max_length=128, null=True)),
                ('from_user_id', models.CharField(max_length=24, null=True)),
                ('on_track_url', models.TextField(default='')),
                ('to_user_id', models.CharField(max_length=24, null=True)),
                ('to_user_name', models.CharField(max_length=128, null=True)),
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
                ('message', models.TextField(null=True)),
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
                ('amount', models.DecimalField(max_digits=50, decimal_places=8)),
                ('pending', models.BooleanField(default=True)),
                ('confirmations', models.IntegerField(default=0)),
                ('txid', models.CharField(max_length=64)),
                ('user', models.ForeignKey(to='core.User', null=True)),
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
            field=models.ForeignKey(related_name='transaction_to_users', to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='deposit_address',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=24, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='deposit_address',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(unique=True, max_length=24),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(max_digits=50, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(default=0, null=True, max_digits=50, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(max_digits=50, decimal_places=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(default=0, null=True, max_digits=50, decimal_places=8),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='to_user_temp_id',
            field=models.CharField(max_length=24, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='parent_transaction',
            field=models.ForeignKey(to='core.Transaction', null=True),
            preserve_default=True,
        ),
    ]
