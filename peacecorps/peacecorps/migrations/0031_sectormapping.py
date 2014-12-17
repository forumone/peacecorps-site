# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0030_auto_20141103_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectorMapping',
            fields=[
                ('accounting_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('campaign', models.ForeignKey(to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
