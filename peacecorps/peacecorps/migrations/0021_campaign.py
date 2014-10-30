# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0020_auto_20141028_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('campaigntype', models.CharField(choices=[('coun', 'Country'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('tag', 'Tag')], max_length=10)),
                ('tagline', models.CharField(null=True, blank=True, max_length=140, help_text='a short phrase for banners (140 characters)')),
                ('call', models.CharField(null=True, blank=True, max_length=50, help_text='call to action for buttons (50 characters)')),
                ('slug', models.SlugField(unique=True, max_length=100, help_text='used for the fund page url.')),
                ('description', tinymce.models.HTMLField()),
                ('featured_image', models.ForeignKey(blank=True, help_text='A large landscape image for use in banners, headers, etc', null=True, to='peacecorps.Media')),
                ('fund', models.ForeignKey(unique=True, blank=True, null=True, to='peacecorps.Fund')),
                ('icon', models.ForeignKey(blank=True, help_text='A small icon to represent the issue on the landing page.', null=True, to='peacecorps.Media', related_name='campaign-icon')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
