# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askKruglov_app', '0020_answer_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='lalala',
            field=models.IntegerField(default=0),
        ),
    ]
