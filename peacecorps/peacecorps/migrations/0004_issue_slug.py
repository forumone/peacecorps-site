# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20141003_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='slug',
            field=models.CharField(blank=True, null=True, max_length=100, help_text='used for the issue page url.', unique=True),
            preserve_default=True,
        ),
    ]
