# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0035_auto_20141202_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='accountnew',
            field=models.ForeignKey(blank=True, to='peacecorps.Account', related_name='cam', null=True, unique=True, to_field='code'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='accountnew',
            field=models.ForeignKey(blank=True, to='peacecorps.Account', related_name='proj', null=True, unique=True, to_field='code'),
            preserve_default=True,
        ),
    ]
