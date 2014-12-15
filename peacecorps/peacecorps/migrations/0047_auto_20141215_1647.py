# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def oncode(apps, schema_editor):
    FeaturedProjectFrontPage = apps.get_model("peacecorps",
                                              "FeaturedProjectFrontPage")
    FeaturedCampaign = apps.get_model("peacecorps", "FeaturedCampaign")

    for fproj in FeaturedProjectFrontPage.objects.all():
        fproj.projid = fproj.project
        fproj.save()

    for fcam in FeaturedCampaign.objects.all():
        fcam.accountid = fcam.campaign
        fcam.save()

def onpk(apps, schema_editor):
    FeaturedProjectFrontPage = apps.get_model("peacecorps",
                                              "FeaturedProjectFrontPage")
    FeaturedCampaign = apps.get_model("peacecorps", "FeaturedCampaign")

    for fproj in FeaturedProjectFrontPage.objects.all():
        fproj.project = fproj.projid
        fproj.save()

    for fcam in FeaturedCampaign.objects.all():
        fcam.campaign = fcam.accountid
        fcam.save()


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0046_auto_20141215_1629'),
    ]

    operations = [
        migrations.RunPython(oncode, onpk)
    ]
