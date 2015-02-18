# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0002_auto_20150206_2338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='featuredcampaign',
            options={'verbose_name': 'Featured Campaign', 'verbose_name_plural': 'Featured Campaign'},
        ),
        migrations.AlterModelOptions(
            name='featuredprojectfrontpage',
            options={'verbose_name': 'Featured Project', 'verbose_name_plural': 'Featured Projects'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'Media'},
        ),
        migrations.AddField(
            model_name='campaign',
            name='featured_image',
            field=models.ForeignKey(to='peacecorps.Media', null=True, blank=True, related_name='campaign-headers', help_text='A large landscape image for use in banners, headers, etc'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(to='peacecorps.Media', null=True, blank=True, related_name='campaign-icons', help_text='A small photo shown on listing pages'),
        ),
    ]
