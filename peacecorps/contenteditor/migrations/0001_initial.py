# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def createExtraUserFields(apps, schema_editor):
    user_model = settings.AUTH_USER_MODEL.split(".")
    for user in apps.get_model(user_model[0], user_model[1]).objects.all():
        apps.get_model("contenteditor", "ExtraUserFields").objects.create(
            user=user, last_password_change=user.date_joined)


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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('last_password_change', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(createExtraUserFields, deleteExtraUserFields),
    ]
