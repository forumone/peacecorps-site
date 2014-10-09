# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0002_auto_20141003_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedProjectFrontPage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(to='peacecorps.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='FeaturedCampaign',
            new_name='FeaturedIssue',
        ),
        migrations.AddField(
            model_name='project',
            name='issue_feature',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.TextField(help_text="Provide an image description for users with screenreaders.         If the image has text, transcribe the text here. If it's a photo,         briefly describe the scene. For design elements like icons, bullets,         etc, leave this field blank."),
        ),
    ]
