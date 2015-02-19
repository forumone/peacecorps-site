# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20150218_0126'),
        ('site_configuration', '0002_auto_20150219_0221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('intro_text', models.CharField(help_text='Introductory Text at the top of the donations landing page.', max_length=255)),
                ('about_donating', models.CharField(help_text='Text about how donating supports projects.', max_length=255)),
                ('featured_image', models.ForeignKey(help_text='A large landscape image for the top of the page', blank=True, to='peacecorps.Media', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
