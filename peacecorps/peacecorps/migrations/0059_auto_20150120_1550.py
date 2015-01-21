# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.db import migrations

from peacecorps.management.commands.sync_accounting import clean_description


def clean(apps, schema_editor):
    """Cleans the description field for imported projects/funds"""
    for campaign in apps.get_model("peacecorps", "Campaign").objects.all():
        campaign.description = clean_description(campaign.description)
        campaign.description = re.sub(r"(?<!\\)\n", r"\\n",
                                      campaign.description)
        campaign.save()

    for project in apps.get_model("peacecorps", "Project").objects.all():
        project.description = clean_description(project.description)
        project.description = re.sub(r"(?<!\\)\n", r"\\n", project.description)
        project.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0058_remove_project_volunteerhomecity'),
    ]

    operations = [
        migrations.RunPython(clean, noop)
    ]
