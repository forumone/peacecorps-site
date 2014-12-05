# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sirtrevor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0035_auto_20141202_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vignette',
            fields=[
                ('slug', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('location', models.TextField()),
                ('instructions', models.TextField()),
                ('content', sirtrevor.fields.SirTrevorField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
