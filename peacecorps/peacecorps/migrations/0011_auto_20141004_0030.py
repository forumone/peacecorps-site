# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0010_auto_20141003_2345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='fundtotal',
            new_name='fundgoal',
        ),
        migrations.AddField(
            model_name='project',
            name='tagline',
            field=models.CharField(default='This is the project subheading.', max_length=240, help_text='a short description for subheadings.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text='the full description.'),
        ),
    ]
