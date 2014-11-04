# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0028_auto_20141031_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ForeignKey(to='peacecorps.Media', null=True, help_text='A large landscape image for use in banners, headers, etc'),
        ),
    ]
