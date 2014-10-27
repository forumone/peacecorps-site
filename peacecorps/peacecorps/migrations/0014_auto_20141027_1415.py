# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0013_donorinfo_xml'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemorialFund',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=100, unique=True, help_text='used for the fund page url.')),
                ('description', tinymce.models.HTMLField()),
                ('featured_image', models.ForeignKey(blank=True, to='peacecorps.Media', null=True, help_text='A large landscape image for use in banners, headers, etc')),
                ('fund', models.ForeignKey(to='peacecorps.Fund', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='fund',
            name='name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
