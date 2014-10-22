# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps


class Migration(migrations.Migration):

    dependencies = [
        ('paygov', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donorinfo',
            name='expires_at',
            field=models.DateTimeField(default=peacecorps.models.default_expire_time),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donorinfo',
            name='fund',
            field=models.ForeignKey(related_name='donorinfos', to='peacecorps.Fund'),
        ),
    ]
