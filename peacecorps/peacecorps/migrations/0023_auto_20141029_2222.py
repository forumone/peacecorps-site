# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0022_auto_20141029_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='campaigns',
            field=models.ManyToManyField(null=True, blank=True, help_text='Campaigns to which this project belongs', to='peacecorps.Campaign'),
        ),
    ]
