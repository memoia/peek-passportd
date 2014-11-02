# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141102_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='group_name',
            field=models.CharField(default=b'Unknown', max_length=256),
            preserve_default=True,
        ),
    ]
