# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0010_auto_20150316_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayGovAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('message', tinymce.models.HTMLField(help_text='A message for the Pay.gov alert.')),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
