# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20141129_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mention',
            old_name='by_user_id',
            new_name='from_user_id',
        ),
        migrations.RenameField(
            model_name='mention',
            old_name='by_user_name',
            new_name='from_user_name',
        ),
    ]
