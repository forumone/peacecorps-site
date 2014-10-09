# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0008_issue_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='call',
            field=models.CharField(help_text='call to action for buttons (40 characters)', max_length=40, default="donate to girl's education."),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='tagline',
            field=models.CharField(help_text='a short phrase for banners (140 characters)', max_length=140),
        ),
    ]
