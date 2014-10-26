# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0011_auto_20141022_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donorinfo',
            name='xml',
        ),
    ]
