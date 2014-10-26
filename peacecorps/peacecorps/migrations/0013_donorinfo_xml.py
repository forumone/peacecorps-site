# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import peacecorps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0012_remove_donorinfo_xml'),
    ]

    operations = [
        migrations.AddField(
            model_name='donorinfo',
            name='xml',
            field=peacecorps.fields.GPGField(default=b'', gpg_check=True),
            preserve_default=False,
        ),
    ]
