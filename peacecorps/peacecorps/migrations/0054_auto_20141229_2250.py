# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0053_remove_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='slug',
            field=models.SlugField(null=True, help_text='anchor', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='current',
            field=models.IntegerField(default=0, help_text='Amount from donations (excluding real-time), in cents'),
        ),
        migrations.AlterField(
            model_name='account',
            name='goal',
            field=models.IntegerField(null=True, help_text='Donations goal (excluding community contribution)', blank=True),
        ),
    ]
