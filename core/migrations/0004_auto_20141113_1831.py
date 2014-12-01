# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141105_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deposit_address',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
