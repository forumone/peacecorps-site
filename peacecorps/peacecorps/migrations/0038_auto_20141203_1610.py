# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0037_auto_20141203_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='account',
        ),
        migrations.RemoveField(
            model_name='project',
            name='account',
        ),
    ]
