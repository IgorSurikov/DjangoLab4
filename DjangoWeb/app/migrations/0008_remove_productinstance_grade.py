# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-02 12:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200402_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinstance',
            name='grade',
        ),
    ]
