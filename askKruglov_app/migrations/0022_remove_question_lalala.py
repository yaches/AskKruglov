# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 08:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askKruglov_app', '0021_question_lalala'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='lalala',
        ),
    ]
