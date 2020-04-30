# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-30 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200330_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, choices=[('зерномучные товары', 'зерномучные товары'), ('фрукты, овощи, грибы', 'фрукты, овощи, грибы'), ('крахмалопродукты, сахар, мед, кондитерские изделия', 'крахмалопродукты, сахар, мед, кондитерские изделия'), ('пищевые жиры', 'пищевые жиры'), ('мясо и мясные товары', 'мясо и мясные товары'), ('рыба, морепродукты, рыбная продукция', 'рыба, морепродукты, рыбная продукция'), ('молочные продукты', 'молочные продукты'), ('яйца и яичные товары', 'яйца и яичные товары')], help_text='тип продукта', max_length=100),
        ),
    ]
