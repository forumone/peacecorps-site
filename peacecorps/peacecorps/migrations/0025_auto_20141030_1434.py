# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0024_auto_20141029_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countryfund',
            name='country',
        ),
        migrations.RemoveField(
            model_name='countryfund',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='countryfund',
            name='fund',
        ),
        migrations.DeleteModel(
            name='CountryFund',
        ),
        migrations.RemoveField(
            model_name='featuredissue',
            name='issue',
        ),
        migrations.DeleteModel(
            name='FeaturedIssue',
        ),
        migrations.RemoveField(
            model_name='funddisplay',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='funddisplay',
            name='fund',
        ),
        migrations.DeleteModel(
            name='FundDisplay',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='fund',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='memorialfund',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='memorialfund',
            name='fund',
        ),
        migrations.RemoveField(
            model_name='memorialfund',
            name='headshot',
        ),
        migrations.DeleteModel(
            name='MemorialFund',
        ),
        migrations.RemoveField(
            model_name='project',
            name='issue',
        ),
        migrations.RemoveField(
            model_name='project',
            name='issue_feature',
        ),
        migrations.RemoveField(
            model_name='project',
            name='issues_related',
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(help_text='A small icon to represent this on the landing page.', related_name='campaign-icon', null=True, blank=True, to='peacecorps.Media'),
        ),
    ]
