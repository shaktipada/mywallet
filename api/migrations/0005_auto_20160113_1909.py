# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160111_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mywallet',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='mywallet',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 13, 19, 9, 12, 571019, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mywallet',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 13, 19, 9, 29, 110762, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
