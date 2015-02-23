# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_configuration', '0004_auto_20150219_0225'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitewideNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('enable', models.BooleanField(default=False, help_text='Enables the Sitewide Announcement.')),
                ('header', models.CharField(max_length=100, help_text='The Header Text for the current site-wide announcement.')),
                ('body', models.TextField(max_length=255, help_text='The body text for the site-wide announcement, viewable on first page load.')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
