# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0009_auto_20141022_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='homecity',
            new_name='volunteerhomecity',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='homestate',
            new_name='volunteerhomestate',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='profile_image',
            new_name='volunteerpicture',
        ),
        migrations.RemoveField(
            model_name='project',
            name='volunteer',
        ),
        migrations.AlterField(
            model_name='project',
            name='volunteername',
            field=models.CharField(max_length=100),
        ),
    ]
