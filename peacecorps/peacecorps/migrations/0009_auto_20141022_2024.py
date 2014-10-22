# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0008_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='homecity',
            field=models.CharField(null=True, blank=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='homestate',
            field=localflavor.us.models.USPostalCodeField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], null=True, blank=True, max_length=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='profile_image',
            field=models.ForeignKey(related_name='volunteer', to='peacecorps.Media', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='volunteername',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countryfund',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=tinymce.models.HTMLField(help_text='the full description.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='issues_related',
            field=models.ManyToManyField(related_name='related_projects', help_text='other issues this project relates to.', null=True, blank=True, to='peacecorps.Issue'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='profile_image',
            field=models.ForeignKey(related_name='volunteerimage', to='peacecorps.Media', null=True, blank=True),
        ),
    ]
