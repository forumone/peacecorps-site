# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0025_auto_20141030_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('code', models.CharField(max_length=25, unique=True)),
                ('current', models.IntegerField(default=0)),
                ('goal', models.IntegerField(null=True, blank=True)),
                ('community_contribution', models.IntegerField(null=True, blank=True)),
                ('category', models.CharField(max_length=10, choices=[('coun', 'Country'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('proj', 'Project')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='fund',
            old_name='fundtype',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fundoverflow',
        ),
        migrations.AddField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(to='peacecorps.Account', null=True, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donation',
            name='account',
            field=models.ForeignKey(related_name='donations', null=True, blank=True, to='peacecorps.Account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donorinfo',
            name='account',
            field=models.ForeignKey(related_name='donorinfos', null=True, blank=True, to='peacecorps.Account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='account',
            field=models.ForeignKey(to='peacecorps.Account', null=True, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='overflow',
            field=models.ForeignKey(related_name='overflow', null=True, blank=True, to='peacecorps.Account'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(max_length=100, help_text='used for the campaign page url.', unique=True),
        ),
    ]
