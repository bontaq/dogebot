# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141118_0006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mention',
            old_name='user_id',
            new_name='by_user_id',
        ),
        migrations.RenameField(
            model_name='mention',
            old_name='user_name',
            new_name='by_user_name',
        ),
        migrations.AddField(
            model_name='mention',
            name='on_track_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mention',
            name='to_user_id',
            field=models.CharField(max_length=24, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mention',
            name='to_user_name',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mention',
            name='timestamp',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
