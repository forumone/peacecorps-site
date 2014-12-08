# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0036_vignette'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('icon', models.FileField(upload_to='')),
                ('campaigns', models.ManyToManyField(to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
