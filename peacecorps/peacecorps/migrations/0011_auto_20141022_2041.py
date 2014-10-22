# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0010_auto_20141022_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='media',
            name='author',
        ),
        migrations.DeleteModel(
            name='Volunteer',
        ),
    ]
