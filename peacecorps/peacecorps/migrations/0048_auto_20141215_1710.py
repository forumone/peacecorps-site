# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0047_auto_20141215_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredcampaign',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='featuredprojectfrontpage',
            name='project',
        ),
        migrations.AlterField(
            model_name='featuredcampaign',
            name='accountid',
            field=models.ForeignKey(to='peacecorps.Campaign', to_field='account'),
        ),
        migrations.AlterField(
            model_name='featuredprojectfrontpage',
            name='projid',
            field=models.ForeignKey(to='peacecorps.Project', to_field='account'),
        ),
    ]
