# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_configuration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donate',
            name='featured_image',
        ),
        migrations.DeleteModel(
            name='Donate',
        ),
    ]
