# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0007_donorinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('fund', models.ForeignKey(related_name='donations', to='peacecorps.Fund')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
