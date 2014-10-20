# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0004_countryfund_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryfund',
            name='description',
            field=models.TextField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='countryfund',
            name='slug',
            field=models.SlugField(unique=True, help_text='used for the issue page url.', max_length=100),
        ),
    ]
