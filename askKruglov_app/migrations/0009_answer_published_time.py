# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('askKruglov_app', '0008_auto_20161114_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='published_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
