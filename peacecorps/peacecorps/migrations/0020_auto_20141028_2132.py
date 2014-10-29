# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0019_auto_20141028_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fundcode',
            field=models.CharField(unique=True, max_length=25),
        ),
    ]
