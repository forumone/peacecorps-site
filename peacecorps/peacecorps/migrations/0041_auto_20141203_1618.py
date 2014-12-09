# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0040_auto_20141203_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.ForeignKey(unique=True, to_field='code', to='peacecorps.Account'),
        ),
    ]
