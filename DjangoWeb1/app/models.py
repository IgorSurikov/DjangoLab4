
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    PRODUCT_TYPE = (
        ('зерномучные товары', 'зерномучные товары'),
        ('фрукты, овощи, грибы', 'фрукты, овощи, грибы'),
        ('крахмалопродукты, сахар, мед, кондитерские изделия',
         'крахмалопродукты, сахар, мед, кондитерские изделия'),
        ('пищевые жиры', 'пищевые жиры'),
        ('мясо и мясные товары', 'мясо и мясные товары'),
        ('рыба, морепродукты, рыбная продукция',
         'рыба, морепродукты, рыбная продукция'),
        ('молочные продукты', 'молочные продукты'),
        ('яйца и яичные товары', 'яйца и яичные товары'),
    )
    product_type = models.CharField(
        max_length=100,
        choices=PRODUCT_TYPE,
        blank=True,
        help_text='тип продукта')
    description = models.TextField(
        max_length=1000, help_text="описание продукта", blank=True)

    def __str__(self):
        return self.product_name


class ProductGrade(models.Model):
    calories = models.FloatField(help_text='калории на 100 грамм')
    grade_name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, help_text="описание сорта")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.grade_name


class ProductInstance(models.Model):
    weight = models.FloatField(help_text='количество в граммах')
    grade = models.ForeignKey(
        'ProductGrade', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.grade.grade_name


class Result(models.Model):
    GENDER = (('M', 'Мужчина'), ('W', 'Женщина'))
    gender = models.CharField(max_length=100, choices=GENDER)
    weight = models.FloatField(null=True)
    height = models.IntegerField(null=True)
