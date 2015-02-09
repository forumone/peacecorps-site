# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0001_squashed_0061'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='published',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaigntype',
            field=models.CharField(choices=[('coun', 'Country'), ('gen', 'General'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other')], max_length=10),
        ),
    ]
