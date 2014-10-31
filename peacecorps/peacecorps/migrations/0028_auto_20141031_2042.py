# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0027_auto_20141031_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='fund',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='fund',
        ),
        migrations.RemoveField(
            model_name='donorinfo',
            name='fund',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fund',
        ),
        migrations.DeleteModel(
            name='Fund',
        ),
        migrations.AlterField(
            model_name='donation',
            name='account',
            field=models.ForeignKey(related_name='donations', to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='donorinfo',
            name='account',
            field=models.ForeignKey(related_name='donorinfos', to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.ForeignKey(to='peacecorps.Account', unique=True),
        ),
    ]
