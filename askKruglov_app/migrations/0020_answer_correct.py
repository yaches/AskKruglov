# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askKruglov_app', '0019_remove_answer_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]
