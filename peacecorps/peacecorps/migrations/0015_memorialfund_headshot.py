# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0014_auto_20141027_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='memorialfund',
            name='headshot',
            field=models.ForeignKey(to='peacecorps.Media', blank=True, related_name='memorial_headshot', help_text='A picture of the memorialized person', null=True),
            preserve_default=True,
        ),
    ]
