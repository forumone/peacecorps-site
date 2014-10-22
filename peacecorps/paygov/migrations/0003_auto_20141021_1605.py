# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paygov', '0002_auto_20141020_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donorinfo',
            name='fund',
        ),
        migrations.DeleteModel(
            name='DonorInfo',
        ),
    ]
