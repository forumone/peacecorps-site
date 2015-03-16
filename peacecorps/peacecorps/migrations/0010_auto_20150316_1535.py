# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.util.svg


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0009_auto_20150313_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredcampaign',
            name='image',
            field=models.ForeignKey(help_text='Image shown on the landing page. 1100px         wide by 589px tall.', to='peacecorps.Media'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='icon',
            field=models.FileField(validators=[peacecorps.util.svg.full_validation], help_text='An SVG file used to represent the issue. The background         should be transparent.', upload_to='icons'),
        ),
        migrations.AlterField(
            model_name='project',
            name='abstract',
            field=models.TextField(null=True, blank=True, help_text='A shorter description, used for quick views of the         project.', max_length=256),
        ),
        migrations.AlterField(
            model_name='project',
            name='campaigns',
            field=models.ManyToManyField(to='peacecorps.Campaign', null=True, blank=True, help_text='The issues this project is associated with.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='country',
            field=models.ForeignKey(related_name='projects', help_text='The country the project is located in. The project will         appear in the Project Sorter under this country.', to='peacecorps.Country'),
        ),
        migrations.AlterField(
            model_name='project',
            name='overflow',
            field=models.ForeignKey(related_name='overflow', help_text="The fund donors will be encourage to contribute to if the         project is fully funded. By default, this is the project's         sector fund.", null=True, blank=True, to='peacecorps.Account'),
        ),
    ]
