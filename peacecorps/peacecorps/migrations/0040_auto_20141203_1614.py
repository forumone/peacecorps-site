# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0039_auto_20141203_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(blank=True, null=True, to_field='code', unique=True, to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.ForeignKey(blank=True, null=True, to_field='code', unique=True, to='peacecorps.Account'),
        ),
    ]
