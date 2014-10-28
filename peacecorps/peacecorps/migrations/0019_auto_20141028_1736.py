# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0018_issue_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='icon',
            field=models.ForeignKey(help_text='A small icon to represent the issue on the landing page.', to='peacecorps.Media', related_name='iconissues'),
        ),
    ]
