# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0043_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='abstract',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
