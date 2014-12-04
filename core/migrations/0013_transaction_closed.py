# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_transaction_parent_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='closed',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
