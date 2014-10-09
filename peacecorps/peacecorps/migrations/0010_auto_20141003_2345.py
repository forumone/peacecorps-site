# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0009_auto_20141003_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='media',
            field=models.ManyToManyField(related_name='projects', blank=True, null=True, to='peacecorps.Media'),
        ),
    ]
