# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0041_auto_20141203_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=peacecorps.fields.BraveSirTrevorField(help_text='the full description.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=peacecorps.fields.BraveSirTrevorField(help_text='the full description.'),
        ),
    ]
