# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-04 14:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20200404_1236'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CleanFlag',
        ),
    ]