# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fundtoaccount(apps, schema_editor):
    Fund = apps.get_model("peacecorps", "Fund")
    Account = apps.get_model("peacecorps", "Account")
    Campaign = apps.get_model("peacecorps", "Campaign")
    Donation = Campaign = apps.get_model("peacecorps", "Donation")
    DonorInfo = Campaign = apps.get_model("peacecorps", "DonorInfo")
    Project = Campaign = apps.get_model("peacecorps", "Project")

    for x in Fund.objects.all():
        account = Account(
            name=x.name,
            code=x.fundcode,
            current=x.fundcurrent,
            goal=x.fundgoal,
            community_contribution=x.community_contribution,
            category=x.category
            )

        account.save()

    for x in Campaign.objects.all():
        x.account = Account.objects.get(name=x.fund.name)
        x.save()

    for x in Donation.objects.all():
        x.account = Account.objects.get(name=x.fund.name)
        x.save()

    for x in DonorInfo.objects.all():
        x.account = Account.objects.get(name=x.fund.name)
        x.save()

    for x in Project.objects.all():
        x.account = Account.objects.get(name=x.fund.name)
        x.save()


def accounttofund(apps, schema_editor):
    # for backwards migrations.
    Fund = apps.get_model("peacecorps", "Fund")
    Account = apps.get_model("peacecorps", "Account")
    Campaign = apps.get_model("peacecorps", "Campaign")
    Donation = Campaign = apps.get_model("peacecorps", "Donation")
    DonorInfo = Campaign = apps.get_model("peacecorps", "DonorInfo")
    Project = Campaign = apps.get_model("peacecorps", "Project")
    
    for x in Account.objects.all():
        fund = Fund(
            name=x.name,
            fundcode=x.code,
            fundcurrent=x.current,
            fundgoal=x.goal,
            community_contribution=x.community_contribution,
            category=x.category
            )

        fund.save()

    for x in Campaign.objects.all():
        x.fund = Fund.objects.get(name=x.account.name)
        x.save()

    for x in Donation.objects.all():
        x.fund = Fund.objects.get(name=x.account.name)
        x.save()

    for x in DonorInfo.objects.all():
        x.fund = Fund.objects.get(name=x.account.name)
        x.save()

    for x in Project.objects.all():
        x.fund = Fund.objects.get(name=x.account.name)
        x.save()

class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0026_auto_20141030_2129'),
    ]

    operations = [
        migrations.RunPython(fundtoaccount, accounttofund),
    ]
