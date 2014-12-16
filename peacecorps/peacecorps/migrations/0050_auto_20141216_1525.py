# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0049_auto_20141215_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='featured_image',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, to='peacecorps.Media', help_text='A small photo to represent this on the landing page.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='campaigns',
            field=models.ManyToManyField(blank=True, null=True, to='peacecorps.Campaign', help_text='The campaigns to which this project belongs.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='overflow',
            field=models.ForeignKey(blank=True, null=True, to='peacecorps.Account', help_text='Select another fund to which users will be directed to\n                    donate if the project is already funded.', related_name='overflow'),
        ),
    ]
