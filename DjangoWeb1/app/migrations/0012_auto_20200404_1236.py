# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-04 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
