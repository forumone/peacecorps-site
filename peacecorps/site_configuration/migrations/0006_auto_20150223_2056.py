# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20150218_0126'),
        ('site_configuration', '0005_sitewidenotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='donate',
            name='sorter_featured_image',
            field=models.ForeignKey(blank=True, help_text='A large landscape image for the top of the sorter page', related_name='donate_sorter_featured_image', null=True, to='peacecorps.Media'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donate',
            name='featured_image',
            field=models.ForeignKey(blank=True, help_text='A large landscape image for the top of the page', related_name='donate_landing_featured_image', null=True, to='peacecorps.Media'),
        ),
    ]
