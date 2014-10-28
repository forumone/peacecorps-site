# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0017_remove_issue_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='icon',
            field=models.ForeignKey(to='peacecorps.Media', help_text='A small icon to represent the issue on the landing page.', blank=True, related_name='iconissues', null=True),
            preserve_default=True,
        ),
    ]
