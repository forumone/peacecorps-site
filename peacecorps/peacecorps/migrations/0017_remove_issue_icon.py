# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0016_funddisplay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='icon',
        ),
    ]
