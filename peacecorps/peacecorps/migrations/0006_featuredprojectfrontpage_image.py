# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_image(apps, schema_editor):
    Featured = apps.get_model("peacecorps", "FeaturedProjectFrontPage")
    for featured in Featured.objects.filter(
            project__featured_image__isnull=False):
        featured.image = featured.project.featured_image
        featured.save()


def delete_image(apps, schema_editor):
    Featured = apps.get_model("peacecorps", "FeaturedProjectFrontPage")
    Featured.objects.all().update(image=None)


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0005_auto_20150224_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredprojectfrontpage',
            name='image',
            field=models.ForeignKey(
                null=True, to='peacecorps.Media',
                help_text='Image shown on the landing page. Roughly 525x320'),
            preserve_default=True,
        ),
        migrations.RunPython(copy_image, delete_image),
        migrations.AlterField(
            model_name='featuredprojectfrontpage',
            name='image',
            field=models.ForeignKey(
                to='peacecorps.Media',
                help_text='Image shown on the landing page. Roughly 525x320'),
        ),
    ]
