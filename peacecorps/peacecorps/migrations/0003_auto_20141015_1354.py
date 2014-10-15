# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0002_auto_20141014_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryfund',
            name='fund',
            field=models.ForeignKey(unique=True, to='peacecorps.Fund'),
        ),
        migrations.AlterField(
            model_name='fund',
            name='community_contribution',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fundgoal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='fund',
            field=models.ForeignKey(unique=True, to='peacecorps.Fund'),
        ),
        migrations.AlterField(
            model_name='project',
            name='fund',
            field=models.ForeignKey(unique=True, to='peacecorps.Fund'),
        ),
    ]
