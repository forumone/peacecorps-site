# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0004_issue_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='slug',
            field=models.CharField(help_text='used for the issue page url.', unique=True, max_length=100),
        ),
    ]
