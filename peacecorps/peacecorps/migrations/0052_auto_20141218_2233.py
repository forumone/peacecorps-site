# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0051_auto_20141217_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='icon_background',
            field=models.FileField(upload_to='', help_text='Background used when a large icon is present', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='icon',
            field=models.FileField(upload_to='', help_text='Icon commonly used to represent this issue'),
        ),
    ]
