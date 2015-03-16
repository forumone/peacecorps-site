# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.util.svg
import peacecorps.fields
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0008_auto_20150313_1810'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQs', 'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=peacecorps.fields.BraveSirTrevorField(help_text='The rich text answer to the         question.'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=256, help_text='The question used         as the prompt for the FAQ.'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='slug',
            field=models.SlugField(null=True, help_text='The URL this         should exist at.', blank=True),
        ),
        migrations.AlterField(
            model_name='featuredcampaign',
            name='campaign',
            field=models.ForeignKey(help_text='The campaign to feature.', to_field='account', to='peacecorps.Campaign'),
        ),
        migrations.AlterField(
            model_name='featuredcampaign',
            name='image',
            field=models.ForeignKey(help_text='Image shown on the landing page. 1100px         wide by 475px tall.', to='peacecorps.Media'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='campaigns',
            field=models.ManyToManyField(verbose_name='Sector Funds', to='peacecorps.Campaign', help_text='Sector funds to associate as being under this campaign.'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='icon',
            field=models.FileField(validators=[peacecorps.util.svg.full_validation], help_text='An SVG file used to represent the issue.', upload_to='icons'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='icon_background',
            field=models.FileField(help_text='The background image to use behind the SVG icon. Should be         237px by 237px.', upload_to=''),
        ),
        migrations.AlterField(
            model_name='issue',
            name='name',
            field=models.CharField(max_length=120, help_text='The name of the issue.'),
        ),
        migrations.AlterField(
            model_name='media',
            name='country',
            field=models.ForeignKey(null=True, help_text='The country the photo was taken in.', blank=True, to='peacecorps.Country'),
        ),
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.TextField(help_text="Provide an image description for users with screenreaders.         If the image has text, transcribe the text here. If it's a image,         briefly describe what it depicts. Do not use HTML formatting."),
        ),
        migrations.AlterField(
            model_name='media',
            name='mediatype',
            field=models.CharField(verbose_name='Media Type', max_length=3, default='IMG', choices=[('IMG', 'Image'), ('VID', 'Video'), ('AUD', 'Audio'), ('OTH', 'Other')]),
        ),
        migrations.AlterField(
            model_name='media',
            name='transcript',
            field=models.TextField(null=True, help_text='If the media is a video or audio recording, transcribe it         for users with disabilities.', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='abstract',
            field=models.TextField(null=True, help_text='A shorter description, used for quick views of the         project.', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='account',
            field=models.ForeignKey(help_text='The accounting code for the project.', to='peacecorps.Account', unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='campaigns',
            field=models.ManyToManyField(null=True, help_text='The campaigns this project is related to.', to='peacecorps.Campaign', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='country',
            field=models.ForeignKey(to='peacecorps.Country', help_text='The country the project is located in.', related_name='projects'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=peacecorps.fields.BraveSirTrevorField(help_text='A rich text description         of the project..'),
        ),
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ForeignKey(null=True, help_text='A large landscape image for use on the project page.         Should be 1100px wide and 454px tall.', blank=True, to='peacecorps.Media'),
        ),
        migrations.AlterField(
            model_name='project',
            name='overflow',
            field=models.ForeignKey(null=True, help_text="The fund donors will be encourage to contribute to if the         project is fully funded. If no fund is selected, the default is the         project's sector fund.", blank=True, related_name='overflow', to='peacecorps.Account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='published',
            field=models.BooleanField(default=False, help_text='If selected,         the project will be visible to the public.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=120, help_text='Automatically generated, use for the                             project URL.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tagline',
            field=models.CharField(null=True, max_length=240, help_text='A short title, used as a subheading on the         home page.', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=120, help_text='The title of the project.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='volunteerhomestate',
            field=localflavor.us.models.USPostalCodeField(verbose_name='Volunteer Home State', null=True, max_length=2, help_text='The home state of the Volunteer.', blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='volunteername',
            field=models.CharField(verbose_name='Volunteer Name', max_length=120, help_text='The name of the PCV requesting funds for the project.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='volunteerpicture',
            field=models.ForeignKey(verbose_name='Volunteer Picture', null=True, help_text='A picture of the PCV requesting funds for the project.         Should be 175px by 175px.', blank=True, related_name='volunteer', to='peacecorps.Media'),
        ),
    ]
