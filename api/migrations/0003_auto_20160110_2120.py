# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_biller_unload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biller',
            name='unload',
        ),
        migrations.AddField(
            model_name='biller',
            name='commission',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='biller',
            name='unloaded_amount',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='biller',
            name='wallet',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
