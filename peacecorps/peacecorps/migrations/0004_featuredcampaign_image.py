# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def delete_existing(apps, schema_editor):
    FeaturedCampaign = apps.get_model("peacecorps", "FeaturedCampaign")
    FeaturedCampaign.objects.all().delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0003_auto_20150218_0126'),
    ]

    operations = [
        migrations.RunPython(delete_existing, noop),
        migrations.AddField(
            model_name='featuredcampaign',
            name='image',
            field=models.ForeignKey(
                to='peacecorps.Media',
                help_text='Image shown on the landing page. Roughly 1100x640'),
            preserve_default=False,
        ),
    ]
