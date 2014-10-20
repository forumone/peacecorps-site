# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20141015_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryfund',
            name='slug',
            field=models.SlugField(max_length=100, help_text='used for the issue page url.', default='slug1'),
            preserve_default=False,
        ),
    ]
