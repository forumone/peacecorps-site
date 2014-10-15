# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countryfund',
            name='fundcurrent',
        ),
        migrations.RemoveField(
            model_name='countryfund',
            name='fundgoal',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='description',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='fundcurrent',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='fundgoal',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fundcurrent',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fundgoal',
        ),
        migrations.AddField(
            model_name='countryfund',
            name='featured_image',
            field=models.ForeignKey(null=True, blank=True, help_text='A large landscape image for use in banners, headers, etc', to='peacecorps.Media'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='countryfund',
            name='fund',
            field=models.ForeignKey(unique=True, null=True, blank=True, to='peacecorps.Fund'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fund',
            name='community_contribution',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fund',
            name='fundcode',
            field=models.CharField(max_length=25, default='FAKECODE-011'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fund',
            name='fundtype',
            field=models.CharField(choices=[('coun', 'Country'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('proj', 'Project')], max_length=10, default='oth'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='fund',
            field=models.ForeignKey(unique=True, null=True, blank=True, to='peacecorps.Fund'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='fund',
            field=models.ForeignKey(unique=True, null=True, blank=True, to='peacecorps.Fund'),
            preserve_default=True,
        ),
    ]
