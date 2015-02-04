# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sirtrevor.fields
import peacecorps.fields
import peacecorps.models
import tinymce.models
import localflavor.us.models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# peacecorps.migrations.0034_auto_20141130_2254
# peacecorps.migrations.0047_auto_20141215_1647
# peacecorps.migrations.0027_auto_20141031_2022
# peacecorps.migrations.0037_auto_20141203_1600
# peacecorps.migrations.0030_auto_20141103_1918

class Migration(migrations.Migration):

    replaces = [('peacecorps', '0001_initial'), ('peacecorps', '0002_auto_20141014_2136'), ('peacecorps', '0003_auto_20141015_1354'), ('peacecorps', '0004_countryfund_slug'), ('peacecorps', '0005_auto_20141016_1641'), ('peacecorps', '0006_auto_20141020_1344'), ('peacecorps', '0007_donorinfo'), ('peacecorps', '0008_donation'), ('peacecorps', '0009_auto_20141022_2024'), ('peacecorps', '0010_auto_20141022_2037'), ('peacecorps', '0011_auto_20141022_2041'), ('peacecorps', '0012_remove_donorinfo_xml'), ('peacecorps', '0013_donorinfo_xml'), ('peacecorps', '0014_auto_20141027_1415'), ('peacecorps', '0015_memorialfund_headshot'), ('peacecorps', '0016_funddisplay'), ('peacecorps', '0017_remove_issue_icon'), ('peacecorps', '0018_issue_icon'), ('peacecorps', '0019_auto_20141028_1736'), ('peacecorps', '0020_auto_20141028_2132'), ('peacecorps', '0021_campaign'), ('peacecorps', '0022_auto_20141029_2150'), ('peacecorps', '0023_auto_20141029_2222'), ('peacecorps', '0024_auto_20141029_2251'), ('peacecorps', '0025_auto_20141030_1434'), ('peacecorps', '0026_auto_20141030_2129'), ('peacecorps', '0027_auto_20141031_2022'), ('peacecorps', '0028_auto_20141031_2042'), ('peacecorps', '0029_auto_20141103_1908'), ('peacecorps', '0030_auto_20141103_1918'), ('peacecorps', '0031_sectormapping'), ('peacecorps', '0032_auto_20141124_1853'), ('peacecorps', '0032_auto_20141119_0402'), ('peacecorps', '0033_merge'), ('peacecorps', '0034_auto_20141130_2254'), ('peacecorps', '0035_auto_20141202_2354'), ('peacecorps', '0036_auto_20141203_1559'), ('peacecorps', '0037_auto_20141203_1600'), ('peacecorps', '0038_auto_20141203_1610'), ('peacecorps', '0039_auto_20141203_1613'), ('peacecorps', '0040_auto_20141203_1614'), ('peacecorps', '0041_auto_20141203_1618'), ('peacecorps', '0042_auto_20141208_2209'), ('peacecorps', '0036_vignette'), ('peacecorps', '0037_issue'), ('peacecorps', '0043_merge'), ('peacecorps', '0044_project_abstract'), ('peacecorps', '0045_faq'), ('peacecorps', '0046_auto_20141215_1629'), ('peacecorps', '0047_auto_20141215_1647'), ('peacecorps', '0048_auto_20141215_1710'), ('peacecorps', '0049_auto_20141215_1711'), ('peacecorps', '0050_auto_20141216_1525'), ('peacecorps', '0050_auto_20141216_1525'), ('peacecorps', '0055_auto_20150105_1814'), ('peacecorps', '0051_auto_20141217_1551'), ('peacecorps', '0056_auto_20150109_1852'), ('peacecorps', '0052_auto_20141218_2233'), ('peacecorps', '0057_auto_20150109_1859'), ('peacecorps', '0053_remove_account_id'), ('peacecorps', '0058_remove_project_volunteerhomecity'), ('peacecorps', '0054_auto_20141229_2250'), ('peacecorps', '0059_auto_20150120_1550'), ('peacecorps', '0060_auto_20150120_1630'), ('peacecorps', '0061_campaign_abstract')]
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('name', models.CharField(unique=True, max_length=120)),
                ('code', models.CharField(serialize=False, primary_key=True, max_length=25)),
                ('current', models.IntegerField(default=0, help_text='Amount from donations (excluding real-time), in cents')),
                ('goal', models.IntegerField(blank=True, null=True, help_text='Donations goal (excluding community contribution)')),
                ('community_contribution', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('coun', 'Country'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('proj', 'Project')], max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('campaigntype', models.CharField(choices=[('coun', 'Country'), ('gen', 'General'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('tag', 'Tag')], max_length=10)),
                ('tagline', models.CharField(blank=True, null=True, help_text='a short phrase for banners (140 characters)', max_length=140)),
                ('call', models.CharField(blank=True, null=True, help_text='call to action for buttons (50 characters)', max_length=50)),
                ('slug', models.SlugField(help_text='Auto-generated. Used for the campaign page url.', unique=True, max_length=120)),
                ('description', peacecorps.fields.BraveSirTrevorField(help_text='the full description.')),
                ('abstract', models.TextField(blank=True, null=True)),
                ('account', models.ForeignKey(to='peacecorps.Account', unique=True)),
            ],
            options={
            },
            bases=(models.Model, peacecorps.models.AbstractHTMLMixin),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(to='peacecorps.Account', related_name='donations')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DonorInfo',
            fields=[
                ('agency_tracking_id', models.CharField(serialize=False, primary_key=True, max_length=21)),
                ('xml', peacecorps.fields.GPGField()),
                ('expires_at', models.DateTimeField(default=peacecorps.models.default_expire_time)),
                ('account', models.ForeignKey(to='peacecorps.Account', related_name='donorinfos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=256)),
                ('answer', peacecorps.fields.BraveSirTrevorField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(blank=True, null=True, help_text='anchor')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('campaign', models.ForeignKey(to_field='account', to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturedProjectFrontPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('icon', models.FileField(help_text='Icon commonly used to represent this issue', validators=[peacecorps.util.svg.full_validation], upload_to='icons')),
                ('icon_background', models.FileField(help_text='Background used when a large icon is present', upload_to='')),
                ('campaigns', models.ManyToManyField(to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('file', models.FileField(upload_to='')),
                ('mediatype', models.CharField(default='IMG', max_length=3, choices=[('IMG', 'Image'), ('VID', 'Video'), ('AUD', 'Audio'), ('OTH', 'Other')])),
                ('caption', models.TextField(blank=True, null=True)),
                ('description', models.TextField(help_text="Provide an image description for users with screenreaders.         If the image has text, transcribe the text here. If it's a photo,         briefly describe what it depicts. Do not use html formatting.")),
                ('transcript', models.TextField(blank=True, null=True, help_text='Please transcribe audio for users with disabilities.')),
                ('country', models.ForeignKey(to='peacecorps.Country', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('tagline', models.CharField(blank=True, null=True, help_text='a short description for subheadings.', max_length=240)),
                ('slug', models.SlugField(help_text='for the project url.', max_length=120)),
                ('description', peacecorps.fields.BraveSirTrevorField(help_text='the full description.')),
                ('volunteername', models.CharField(max_length=120)),
                ('volunteerhomestate', localflavor.us.models.USPostalCodeField(blank=True, null=True, max_length=2, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MH', 'Marshall Islands'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PW', 'Palau'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('abstract', models.TextField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to='peacecorps.Account', unique=True)),
                ('campaigns', models.ManyToManyField(blank=True, null=True, help_text='The campaigns to which this project belongs.', to='peacecorps.Campaign')),
                ('country', models.ForeignKey(to='peacecorps.Country', related_name='projects')),
                ('featured_image', models.ForeignKey(to='peacecorps.Media', blank=True, null=True, help_text='A large landscape image for use in banners, headers, etc')),
                ('media', models.ManyToManyField(blank=True, null=True, to='peacecorps.Media', related_name='projects')),
                ('overflow', models.ForeignKey(to='peacecorps.Account', related_name='overflow', blank=True, null=True, help_text='Select another fund to which users will be directed to\n                    donate if the project is already funded.')),
                ('volunteerpicture', models.ForeignKey(to='peacecorps.Media', related_name='volunteer', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model, peacecorps.models.AbstractHTMLMixin),
        ),
        migrations.CreateModel(
            name='SectorMapping',
            fields=[
                ('accounting_name', models.CharField(serialize=False, primary_key=True, max_length=50)),
                ('campaign', models.ForeignKey(to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vignette',
            fields=[
                ('slug', models.CharField(serialize=False, primary_key=True, max_length=50)),
                ('location', models.TextField()),
                ('instructions', models.TextField()),
                ('content', sirtrevor.fields.SirTrevorField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='featuredprojectfrontpage',
            name='project',
            field=models.ForeignKey(to_field='account', to='peacecorps.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='country',
            field=models.ForeignKey(to='peacecorps.Country', related_name='campaign', blank=True, null=True, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='featuredprojects',
            field=models.ManyToManyField(blank=True, null=True, to='peacecorps.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='icon',
            field=models.ForeignKey(to='peacecorps.Media', blank=True, null=True, help_text='A small photo to represent this campaign on the site.'),
            preserve_default=True,
        ),
    ]
