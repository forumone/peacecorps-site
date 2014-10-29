# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0021_campaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.ForeignKey(to='peacecorps.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='campaign',
            name='featurdprojects',
            field=models.ManyToManyField(null=True, blank=True, to='peacecorps.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='campaigns',
            field=models.ManyToManyField(null=True, blank=True, help_text='Campaigns to which this project belongs', to='peacecorps.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='fundoverflow',
            field=models.ForeignKey(null=True, to='peacecorps.Fund', related_name='overflow', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaigntype',
            field=models.CharField(choices=[('coun', 'Country'), ('gen', 'General'), ('sec', 'Sector'), ('mem', 'Memorial'), ('oth', 'Other'), ('tag', 'Tag')], max_length=10),
        ),
    ]
