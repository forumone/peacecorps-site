# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0013_auto_20141006_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='issue',
            name='slug',
            field=models.SlugField(help_text='used for the issue page url.', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(help_text='for the project url.', max_length=100),
        ),
    ]
