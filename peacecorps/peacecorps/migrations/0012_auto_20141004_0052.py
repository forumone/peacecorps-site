# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0011_auto_20141004_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryfund',
            name='fundcurrent',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='countryfund',
            name='fundtotal',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fundcurrent',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fundtotal',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='issue',
            name='fundcurrent',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='issue',
            name='fundgoal',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='fundcurrent',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='fundtotal',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
    ]
