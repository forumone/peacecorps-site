# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0023_auto_20141029_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='featurdprojects',
            new_name='featuredprojects',
        ),
    ]
