# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import contenteditor.models


def createExtraUserFields(apps, schema_editor):
    user_model = settings.AUTH_USER_MODEL.split(".")
    for user in apps.get_model(user_model[0], user_model[1]).objects.all():
        apps.get_model("contenteditor", "ExtraUserFields").objects.create(
            user=user)


def deleteExtraUserFields(apps, schema_editor):
    apps.get_model("contenteditor", "ExtraUserFields").objects.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraUserFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password_expires', models.DateTimeField(default=contenteditor.models.expires)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='extra')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(createExtraUserFields, deleteExtraUserFields),
    ]
