# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0048_auto_20141215_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featuredcampaign',
            old_name='accountid',
            new_name='campaign',
        ),
        migrations.RenameField(
            model_name='featuredprojectfrontpage',
            old_name='projid',
            new_name='project',
        ),
    ]
