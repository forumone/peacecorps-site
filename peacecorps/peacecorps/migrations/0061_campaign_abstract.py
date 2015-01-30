# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0060_auto_20150120_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='abstract',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
