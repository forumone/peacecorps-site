# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0059_auto_20150120_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(help_text='Auto-generated. Used for the campaign page url.', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='issue',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(help_text='for the project url.', max_length=120),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='project',
            name='volunteername',
            field=models.CharField(max_length=120),
        ),
    ]
