# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_squashed_0015_auto_20141215_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuckMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=24)),
                ('message', models.TextField()),
                ('error', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='mention',
            name='on_track_url',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
