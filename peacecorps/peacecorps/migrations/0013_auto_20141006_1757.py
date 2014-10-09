# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0012_auto_20141004_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countryfund',
            name='fundtotal',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='fundtotal',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fundtotal',
        ),
        migrations.AddField(
            model_name='countryfund',
            name='fundgoal',
            field=models.IntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fund',
            name='fundgoal',
            field=models.IntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='fundgoal',
            field=models.IntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='countryfund',
            name='fundcurrent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fundcurrent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='issue',
            name='fundcurrent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='issue',
            name='fundgoal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='fundcurrent',
            field=models.IntegerField(default=0),
        ),
    ]
