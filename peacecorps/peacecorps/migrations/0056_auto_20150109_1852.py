# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def require_account(apps, schema_editor):
    Campaign = apps.get_model("peacecorps", "Campaign")

    #Delete any campaign that doesn't have an assoicated account.

    for campaign in Campaign.objects.all():
        if not campaign.account:
            campaign.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0055_auto_20150105_1814'),
    ]

    operations = [
        migrations.RunPython(require_account),
    ]
