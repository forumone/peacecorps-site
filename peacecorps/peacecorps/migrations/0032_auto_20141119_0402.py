# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0031_sectormapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ForeignKey(help_text='A large landscape image for use in banners, headers, etc', to='peacecorps.Media', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='tagline',
            field=models.CharField(max_length=240, help_text='a short description for subheadings.', null=True, blank=True),
        ),
    ]
