# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0045_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredcampaign',
            name='accountid',
            field=models.ForeignKey(to='peacecorps.Campaign', null=True, to_field='account', blank=True, related_name='featured', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featuredprojectfrontpage',
            name='projid',
            field=models.ForeignKey(to='peacecorps.Project', null=True, to_field='account', blank=True, related_name='featured'),
            preserve_default=True,
        ),
    ]
