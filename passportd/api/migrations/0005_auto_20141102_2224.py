# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20141102_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='duration',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='end_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
