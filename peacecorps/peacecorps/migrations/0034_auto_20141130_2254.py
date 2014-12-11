# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json

def htmltosirtrevor(obj):
    # obj is a Project or Campaign
    try:
        # if it's valid json, it's already sirtrevor-ified
        json.loads(obj.description)
        return False
    except ValueError:
        # if it's not valid json, we need to sirtrevor-ify it.
        sirtrevorobj = {"data":[{"type":"text","data":{"text":""}}]}
        sirtrevorobj['data'][0]['data']['text'] = obj.description
        obj.description = json.dumps(sirtrevorobj)
        obj.save()
    return True


def sirtrevortohtml(obj):
    # obj is a Project or Campaign
    obj.description = obj.description.html
    obj.save()
    return True


def tosirtrevor(apps, schema_editor):
    Project = apps.get_model("peacecorps", "Project")
    Campaign = apps.get_model("peacecorps", "Campaign")

    for proj in Project.objects.all():
        htmltosirtrevor(proj)
    for cam in Campaign.objects.all():
        htmltosirtrevor(cam)


def fromsirtrevor(apps, schema_editor):
    Project = apps.get_model("peacecorps", "Project")
    Campaign = apps.get_model("peacecorps", "Campaign")
    
    for proj in Project.objects.all():
        sirtrevortohtml(proj)
    for cam in Campaign.objects.all():
        sirtrevortohtml(cam)


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0033_merge'),
    ]

    operations = [
        migrations.RunPython(tosirtrevor, fromsirtrevor),
    ]
