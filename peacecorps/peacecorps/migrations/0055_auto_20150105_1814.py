# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.issue_icons


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0054_auto_20141229_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='icon',
            field=models.FileField(validators=[peacecorps.issue_icons.full_validation], upload_to='icons', help_text='Icon commonly used to represent this issue'),
        ),
    ]
