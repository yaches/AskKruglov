# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 16:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askKruglov_app', '0006_tag_popularity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='popularity',
        ),
    ]
