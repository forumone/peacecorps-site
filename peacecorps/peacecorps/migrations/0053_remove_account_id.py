# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_code_cp(model_name, field_name):
    """Copy over accounts from an int id to a str id"""
    def inner(apps, schema_editor):
        for model in apps.get_model("peacecorps", model_name).objects.all():
            try:
                code = getattr(model, field_name).code
                setattr(model, field_name + "_tmp", code)
                model.save()
            except AttributeError: # (overflow can be None)
                setattr(model, field_name + "_tmp", None)
                model.save()
    return inner


def make_rev_code_cp(model_name, field_name):
    """Copy over accounts from an str int id to an int id. As we're only
    dealing with varchars, we'll need to do lookups"""
    def inner(apps, schema_editor):
        for model in apps.get_model("peacecorps", model_name).objects.all():
            try:
                code = getattr(model, field_name + "_tmp")
                setattr(model, field_name,
                        apps.get_model("peacecorps", "account").objects.get(
                            code=code))
                model.save()
            except DoesNotExist: # (overflow can be None)
                setattr(model, field_name, None)
    return inner


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0052_auto_20141218_2233'),
    ]

    operations = [
        # Add temporary, nullable fields
        migrations.AddField(
            model_name='donation',
            name='account_tmp',
            field=models.CharField(null=True, blank=True, max_length=25),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donorinfo',
            name='account_tmp',
            field=models.CharField(null=True, blank=True, max_length=25),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='overflow_tmp',
            field=models.CharField(null=True, blank=True, max_length=25),
            preserve_default=True,
        ),
        # Copy over data
        migrations.RunPython(make_code_cp('Donation', 'account'),
                             make_rev_code_cp('Donation', 'account')),
        migrations.RunPython(make_code_cp('DonorInfo', 'account'),
                             make_rev_code_cp('DonorInfo', 'account')),
        migrations.RunPython(make_code_cp('Project', 'overflow'),
                             make_rev_code_cp('Project', 'overflow')),
        # Remove old fields
        migrations.RemoveField(model_name='donation', name='account'),
        migrations.RemoveField(model_name='donorinfo', name='account'),
        migrations.RemoveField(model_name='project', name='overflow'),
        # Rename fields
        migrations.RenameField(model_name='donation', old_name='account_tmp',
                               new_name='account'),
        migrations.RenameField(model_name='donorinfo', old_name='account_tmp',
                               new_name='account'),
        migrations.RenameField(model_name='project', old_name='overflow_tmp',
                               new_name='overflow'),
        # Convert all other account-referencing fields to charfields (removing
        # fks)
        migrations.AlterField(
            model_name='featuredcampaign',
            name='campaign',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='featuredprojectfrontpage',
            name='project',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='account',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.CharField(max_length=25),
        ),
        # Remove the id field on account
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(max_length=25, serialize=False,
                                   primary_key=True),
        ),
        # Update all references
        migrations.AlterField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(null=True, blank=True, unique=True,
                                    to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='account',
            field=models.ForeignKey(
                related_name='donations', to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='donorinfo',
            name='account',
            field=models.ForeignKey(
                related_name='donorinfos', to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.ForeignKey(unique=True, to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='overflow',
            field=models.ForeignKey(
                null=True, blank=True, related_name='overflow',
                help_text=('Select another fund to which users will be '
                           + 'directed to\n                    donate if '
                           + 'the project is already funded.'),
                to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='featuredcampaign',
            name='campaign',
            field=models.ForeignKey(to='peacecorps.Campaign',
                                    to_field='account'),
        ),
        migrations.AlterField(
            model_name='featuredprojectfrontpage',
            name='project',
            field=models.ForeignKey(to='peacecorps.Project',
                                    to_field='account'),
        ),
    ]
