# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 00:03
from __future__ import unicode_literals

import askMe_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askMe_app', '0011_auto_20161114_2204'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', askMe_app.models.ProfileManager()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='publications',
            field=models.IntegerField(default=0),
        ),
    ]