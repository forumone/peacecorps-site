# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0007_auto_20141003_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='tagline',
            field=models.CharField(default='Two out of three illiterate people are women.', max_length=140),
            preserve_default=False,
        ),
    ]
