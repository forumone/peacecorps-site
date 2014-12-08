# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0037_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='abstract',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
