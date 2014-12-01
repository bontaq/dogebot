# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141113_1841'),
    ]

    operations = [
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
    ]
