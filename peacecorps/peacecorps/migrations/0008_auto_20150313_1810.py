# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0007_auto_20150313_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='abstract',
            field=models.TextField(help_text='A shorter description, used for quick views of the         campaign.', blank=True, null=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(help_text='The accounting code for this campaign.', to='peacecorps.Account', unique=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='call',
            field=models.CharField(help_text='If the campaign is featured on the home         page, this text is used in the button as a Call to Action.', blank=True, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaigntype',
            field=models.CharField(help_text='The type of campaign.', verbose_name='Campaign Type', choices=[('coun', 'Country'), ('gen', 'General'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='country',
            field=models.ForeignKey(related_name='campaign', null=True, help_text='If the campaign is related to a specific country, the ID         of that country.', unique=True, to='peacecorps.Country', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=peacecorps.fields.BraveSirTrevorField(help_text='A rich text description.         of the campaign.'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='featured_image',
            field=models.ForeignKey(related_name='campaign-headers', null=True, help_text='A large landscape image for use at the top of the campaign         page. Should be 1100px wide and 454px tall.', to='peacecorps.Media', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(related_name='campaign-icons', verbose_name='Memorial Fund Volunteer Image', null=True, help_text='Used for Memorial Funds. Typically a picture of the         volunteer. Should be 120px tall and 120px wide, with the focus of the         photo centered.', to='peacecorps.Media', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(help_text='The title for the associated campaign.', max_length=120),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='published',
            field=models.BooleanField(help_text='If published,         the project will be publicly visible on the site.', default=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(help_text='Auto-generated. Used for the campaign page URL.', unique=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='tagline',
            field=models.CharField(help_text='If the campaign is featured on the home page, this text is         used as the description of the campaign.', blank=True, null=True, max_length=140),
        ),
    ]
