# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def accountnew(apps, schema_editor):
    Project = apps.get_model("peacecorps", "Project")
    Campaign = apps.get_model("peacecorps", "Campaign")

    def populate(obj):
        if obj.account:
            obj.accountnew = obj.account
            obj.save()
            return None

    for project in Project.objects.all():
        populate(project)

    for campaign in Campaign.objects.all():
        populate(campaign)

def accountold(apps, schema_editor):
    Project = apps.get_model("peacecorps", "Project")
    Campaign = apps.get_model("peacecorps", "Campaign")  

    def populate(obj):
        if obj.accountnew:
            obj.account = obj.accountnew
            obj.save()
            return None

    for project in Project.objects.all():
        populate(project)

    for campaign in Campaign.objects.all():
        populate(campaign)


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0036_auto_20141203_1559'),
    ]

    operations = [
        migrations.RunPython(accountnew, accountold)
    ]
