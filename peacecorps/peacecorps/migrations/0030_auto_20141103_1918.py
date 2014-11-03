# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def setAllPublish(apps, schema_editor):
    apps.get_model("peacecorps", "Project").objects.update(published=True)


def setAllUnpublish(apps, schema_editor):
    apps.get_model("peacecorps", "Project").objects.update(published=False)


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0029_auto_20141103_1908'),
    ]

    operations = [
        migrations.RunPython(setAllPublish, setAllUnpublish),
    ]
