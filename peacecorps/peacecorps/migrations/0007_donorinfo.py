# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0006_auto_20141020_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorInfo',
            fields=[
                ('agency_tracking_id', models.CharField(serialize=False, primary_key=True, max_length=21)),
                ('xml', models.TextField()),
                ('expires_at', models.DateTimeField(default=peacecorps.models.default_expire_time)),
                ('fund', models.ForeignKey(to='peacecorps.Fund', related_name='donorinfos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
