# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0057_auto_20150109_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='volunteerhomecity',
        ),
    ]
