# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlaBla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bla', models.CharField(max_length=155)),
            ],
        ),
    ]
