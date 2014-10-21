# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20141015_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorInfo',
            fields=[
                ('agency_tracking_id', models.CharField(primary_key=True, max_length=21, serialize=False)),
                ('xml', models.TextField()),
                ('fund', models.ForeignKey(to='peacecorps.Fund')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
