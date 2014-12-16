# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_transaction_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='user',
            field=models.ForeignKey(to='core.User', null=True),
            preserve_default=True,
        ),
    ]
