# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141113_2225'),
    ]

    operations = [
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
            model_name='wallettransaction',
            name='amount',
            field=models.DecimalField(max_digits=50, decimal_places=10),
            preserve_default=True,
        ),
    ]
