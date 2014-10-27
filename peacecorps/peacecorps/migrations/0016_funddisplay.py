# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0015_memorialfund_headshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundDisplay',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(help_text='used for the fund page url.', unique=True, max_length=100)),
                ('description', tinymce.models.HTMLField()),
                ('featured_image', models.ForeignKey(null=True, to='peacecorps.Media', help_text='A large landscape image for use in banners, headers, etc', blank=True)),
                ('fund', models.ForeignKey(unique=True, to='peacecorps.Fund')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
