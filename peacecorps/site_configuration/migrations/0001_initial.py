# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20150218_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('intro_text', models.CharField(max_length=255, help_text='Introductory Text at the top of the donations landing page.')),
                ('about_donating', models.CharField(max_length=255, help_text='Text about how donating supports projects.')),
                ('featured_image', models.ForeignKey(null=True, help_text='A large landscape image for the top of the page', blank=True, to='peacecorps.Media')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
