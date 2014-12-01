# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141102_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mention',
            name='uuid',
            field=models.CharField(unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
