# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sirtrevor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0034_auto_20141130_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='country',
            field=models.ForeignKey(blank=True, to='peacecorps.Country', related_name='campaign', unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=sirtrevor.fields.SirTrevorField(help_text='the full description.'),
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.TextField(help_text="Provide an image description for users with screenreaders.         If the image has text, transcribe the text here. If it's a photo,         briefly describe what it depicts. Do not use html formatting."),
        ),
    ]
