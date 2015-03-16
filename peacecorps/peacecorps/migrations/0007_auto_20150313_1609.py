# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0006_featuredprojectfrontpage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='category',
            field=models.CharField(max_length=10, choices=[('coun', 'Country'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('proj', 'Project')], help_text='The type of         account.'),
        ),
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(max_length=25, serialize=False, primary_key=True, help_text='The accounting code for the project or fund.'),
        ),
        migrations.AlterField(
            model_name='account',
            name='community_contribution',
            field=models.IntegerField(blank=True, null=True, help_text='For PCPP projects, the amount of community contributions,         in cents.'),
        ),
        migrations.AlterField(
            model_name='account',
            name='current',
            field=models.IntegerField(default=0, help_text='Amount from donations (excluding real-time contributions),         in cents.'),
        ),
        migrations.AlterField(
            model_name='account',
            name='goal',
            field=models.IntegerField(blank=True, null=True, help_text='For PCPP projects, the funding goal, excluding community         contribution.'),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(unique=True, max_length=120, help_text='The name of the project or fund.'),
        ),
    ]
