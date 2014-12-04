# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20141129_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='to_user_temp_id',
            field=models.CharField(max_length=24, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_user',
            field=models.ForeignKey(related_name='transaction_to_users', to='core.User', null=True),
            preserve_default=True,
        ),
    ]
