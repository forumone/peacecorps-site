# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryFund',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fundcurrent', models.IntegerField(default=0)),
                ('fundgoal', models.IntegerField()),
                ('country', models.ForeignKey(related_name='fund', to='peacecorps.Country')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedIssue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedProjectFrontPage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(null=True, blank=True)),
                ('fundcurrent', models.IntegerField(default=0)),
                ('fundgoal', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('tagline', models.CharField(max_length=140, help_text='a short phrase for banners (140 characters)')),
                ('call', models.CharField(max_length=40, help_text='call to action for buttons (40 characters)')),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=100, unique=True, help_text='used for the issue page url.')),
                ('icon', models.FileField(null=True, upload_to='', blank=True)),
                ('fundcurrent', models.IntegerField(default=0)),
                ('fundgoal', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='')),
                ('mediatype', models.CharField(max_length=3, default='IMG', choices=[('IMG', 'Image'), ('VID', 'Video'), ('AUD', 'Audio'), ('OTH', 'Other')])),
                ('caption', models.TextField(null=True, blank=True)),
                ('description', models.TextField(help_text="Provide an image description for users with screenreaders.         If the image has text, transcribe the text here. If it's a photo,         briefly describe the scene. For design elements like icons, bullets,         etc, leave this field blank.")),
                ('transcript', models.TextField(null=True, blank=True, help_text='Please transcribe audio for users with disabilities.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('tagline', models.CharField(max_length=240, help_text='a short description for subheadings.')),
                ('slug', models.SlugField(max_length=100, help_text='for the project url.')),
                ('description', models.TextField(help_text='the full description.')),
                ('fundcurrent', models.IntegerField(default=0)),
                ('fundgoal', models.IntegerField()),
                ('issue_feature', models.BooleanField(default=False)),
                ('country', models.ForeignKey(related_name='projects', to='peacecorps.Country')),
                ('featured_image', models.ForeignKey(to='peacecorps.Media', help_text='A large landscape image for use in banners, headers, etc')),
                ('issue', models.ForeignKey(related_name='projects', to='peacecorps.Issue')),
                ('issues_related', models.ManyToManyField(to='peacecorps.Issue', related_name='related_projects', help_text='other issues this project relates to.')),
                ('media', models.ManyToManyField(null=True, to='peacecorps.Media', related_name='projects', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('pronouns', models.CharField(max_length=2, default='T', choices=[('H', 'He'), ('S', 'She'), ('T', 'They')])),
                ('homestate', localflavor.us.models.USPostalCodeField(null=True, max_length=2, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], blank=True)),
                ('homecity', models.CharField(null=True, max_length=120, blank=True)),
                ('profile_image', models.ForeignKey(null=True, to='peacecorps.Media', related_name='volunteer', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='volunteer',
            field=models.ForeignKey(to='peacecorps.Volunteer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='media',
            name='author',
            field=models.ForeignKey(null=True, to='peacecorps.Volunteer', related_name='media', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='media',
            name='country',
            field=models.ForeignKey(null=True, to='peacecorps.Country', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='featured_image',
            field=models.ForeignKey(to='peacecorps.Media', help_text='A large landscape image for use in banners, headers, etc'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fund',
            name='featured_image',
            field=models.ForeignKey(to='peacecorps.Media', help_text='A large landscape image for use in banners, headers, etc'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featuredprojectfrontpage',
            name='project',
            field=models.ForeignKey(to='peacecorps.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featuredissue',
            name='issue',
            field=models.ForeignKey(to='peacecorps.Issue'),
            preserve_default=True,
        ),
    ]
    