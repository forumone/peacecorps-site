# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0005_auto_20141003_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.CharField(max_length=100, null=True, help_text='for the project url.', blank=True),
            preserve_default=True,
        ),
    ]
