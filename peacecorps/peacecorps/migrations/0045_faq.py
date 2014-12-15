# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0044_project_abstract'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('answer', peacecorps.fields.BraveSirTrevorField()),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
    ]
