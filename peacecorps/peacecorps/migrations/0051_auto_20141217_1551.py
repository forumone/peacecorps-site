# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0050_auto_20141216_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(to='peacecorps.Media', help_text='A small photo to represent this campaign on the site.', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(unique=True, max_length=100, help_text='Auto-generated. Used for the campaign page url.'),
        ),
    ]
