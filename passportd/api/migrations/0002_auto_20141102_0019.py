# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='duration',
            field=models.SmallIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
