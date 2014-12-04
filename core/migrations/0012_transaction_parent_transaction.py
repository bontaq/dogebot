# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20141204_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='parent_transaction',
            field=models.ForeignKey(to='core.Transaction', null=True),
            preserve_default=True,
        ),
    ]
