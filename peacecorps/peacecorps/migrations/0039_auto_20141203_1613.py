# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0038_auto_20141203_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='accountnew',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='accountnew',
            new_name='account',
        ),
    ]
