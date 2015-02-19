# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_configuration', '0003_donate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donate',
            name='about_donating',
            field=models.TextField(max_length=255, help_text='Text about how donating supports projects.'),
        ),
        migrations.AlterField(
            model_name='donate',
            name='intro_text',
            field=models.TextField(max_length=255, help_text='Introductory Text at the top of the donations landing page.'),
        ),
    ]
