# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0056_auto_20150109_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(to='peacecorps.Account', unique=True),
        ),
    ]
