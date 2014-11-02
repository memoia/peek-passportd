# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20141102_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='group_name',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='availability',
        ),
    ]
