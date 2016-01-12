# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20160110_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mywallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wallet', models.FloatField(default=0.0)),
                ('contact_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='biller',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='biller',
            name='name',
        ),
        migrations.RemoveField(
            model_name='biller',
            name='wallet',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='wallet',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='amount_involved',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='object_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='biller',
            name='biller',
            field=models.ForeignKey(to='api.Mywallet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='biller',
            name='commission',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='biller',
            name='unloaded_amount',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer',
            field=models.ForeignKey(to='api.Mywallet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='from_user',
            field=models.ForeignKey(related_name='txn_from', to='api.Mywallet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_user',
            field=models.ForeignKey(related_name='txn_towards', to='api.Mywallet'),
            preserve_default=True,
        ),
    ]
