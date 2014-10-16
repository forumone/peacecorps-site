# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peacecorps', '0004_countryfund_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryfund',
            name='description',
            field=models.TextField(default='<p>Proin at sem vel lorem tincidunt lobortis viverra a urna. Praesent at congue mi, sed dignissim arcu. Quisque quis facilisis ligula. Pellentesque dictum est nulla. In sagittis arcu in purus vulputate imperdiet. Proin nec risus lacinia, dignissim felis nec, porta sem. Etiam tortor magna, porta eget dui ut, consequat aliquet dui. Morbi varius laoreet risus, ac auctor magna semper ac. Vestibulum libero dui, tristique non ex sed, condimentum pharetra ex. Nam quis lorem tempor, luctus sapien nec, congue lorem. Nulla elementum vel tortor euismod convallis. Vestibulum aliquet pulvinar lacus id sagittis. Aenean ornare diam ac odio eleifend, vitae fermentum nisl malesuada.</p><p>Duis vitae ullamcorper sem, at vehicula orci. Donec dapibus, enim a posuere tincidunt, turpis arcu tristique odio, sed vestibulum mi ante nec leo. Curabitur hendrerit lacinia ultrices. Aliquam eget lacinia quam. Proin mattis massa massa, vitae vestibulum quam facilisis a. Morbi dolor quam, tempor sit amet scelerisque nec, auctor id eros.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='countryfund',
            name='slug',
            field=models.SlugField(unique=True, help_text='used for the issue page url.', max_length=100),
        ),
    ]
