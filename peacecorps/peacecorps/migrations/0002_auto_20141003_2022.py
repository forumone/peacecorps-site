# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryFund',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('fundcurrent', models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10)),
                ('fundtotal', models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10)),
                ('country', models.ForeignKey(related_name='fund', to='peacecorps.Country')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('fundcurrent', models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10)),
                ('fundtotal', models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10)),
                ('featured_image', models.ForeignKey(help_text='A large landscape image for use in banners, headers, etc', to='peacecorps.Media')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='fundcurrent',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='fundtotal',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, default=0, max_digits=10),
            preserve_default=True,
        ),
    ]
