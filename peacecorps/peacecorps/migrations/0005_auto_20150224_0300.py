# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0004_featuredcampaign_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='abstract',
            field=models.TextField(blank=True, null=True, max_length=256),
        ),
    ]
