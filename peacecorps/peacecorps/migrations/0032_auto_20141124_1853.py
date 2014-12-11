# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sirtrevor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0031_sectormapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=sirtrevor.fields.SirTrevorField(help_text='the full description.'),
        ),
    ]
