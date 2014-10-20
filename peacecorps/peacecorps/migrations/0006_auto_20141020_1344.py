# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0005_auto_20141016_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryfund',
            name='slug',
            field=models.SlugField(unique=True, max_length=100, help_text='used for the fund page url.'),
        ),
    ]
