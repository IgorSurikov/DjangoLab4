from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Product, ProductInstance, ProductGrade, Result
from app.forms import ProductInstanceForm, ResultModelForm, RegistrationForm, LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
import logging


logger = logging.getLogger(__name__)


def log_username(request):
    if request.user.username:
        return request.user.username
    return 'Анонимный пользователь'


def home(request):
    product_list = Product.objects.all()
    product_instance_list = ProductInstance.objects.all()
    logger.info(log_username(request) + " посетил главную страницу")
    return render(
        request, 'app/index.html', {
            'title': 'Home Page',
            'year': datetime.now().year,
            'product_list': product_list,
            'product_instance_list': product_instance_list
        })


def contact(request):
    assert isinstance(request, HttpRequest)
    logger.info(log_username(request) + " посетил страницу контактов")
    return render(
        request, 'app/contact.html', {
            'title': 'Обращаться только по мере необходимости',
            'year': datetime.now().year,
        })


def about(request):
    logger.info(log_username(request) + " посетил страницу об авторе")
    assert isinstance(request, HttpRequest)
    return render(request, 'app/about.html', {
        'title': 'Обо мне',
        'year': datetime.now().year,
    })


def product_grades(request, product_id):
    p = Product.objects.get(id=product_id)
    logger.info(
        log_username(request) + " посетил страницу сортов продукта: " +
        p.product_name)
    product_grades_list = p.productgrade_set.all()
    if request.method == "POST":
        form = ProductInstanceForm(product_grades_list, request.POST)
        if form.is_valid():
            inst_prod = ProductInstance(
                weight=form.cleaned_data['weight'],
                grade=form.cleaned_data['grade'])
            inst_prod.save()
            logger.info(
                log_username(request) + " добавил в список: {0}, вес: {1}".
                format(inst_prod.grade, inst_prod.weight))
            return redirect('home')
    else:
        form = ProductInstanceForm(product_grades_list)
    return render(
        request, 'app/product_grades.html', {
            'title': 'Product grades',
            'year': datetime.now().year,
            'product_grades_list': product_grades_list,
            'form': form
        })


def edit_product(request, instance_id):
    instance = ProductInstance.objects.get(id=instance_id)
    cur_grade = instance.grade
    cur_weight = instance.weight
    p = cur_grade.product
    product_grades_list = p.productgrade_set.all()

    if request.method == "POST":
        form = ProductInstanceForm(product_grades_list, request.POST)
        if form.is_valid():
            instance.weight = form.cleaned_data['weight']
            instance.grade = form.cleaned_data['grade']
            instance.save()
            logger.info(
                log_username(request) +
                " внёс изменения в список. Изменил: Сорт: {0} -> {1}, Вес: {2} -> {3}".
                format(cur_grade, instance.grade, cur_weight, instance.weight))
            return redirect('home')
    else:
        form = ProductInstanceForm(
            product_grades_list,
            initial={
                'weight': instance.weight,
                'grade': cur_grade
            })
    return render(
        request, 'app/edit_product.html', {
            'title': 'Edit product ',
            'year': datetime.now().year,
            'product_grades_list': product_grades_list,
            'form': form
        })


def delete_product(request, instance_id):
    instance = ProductInstance.objects.get(id=instance_id)
    instance.delete()
    logger.info(
        log_username(request) +
        " удалил из списка: {0}".format(instance.grade))
    return redirect('home')


def result(request):
    days_number = None
    result = Result.objects.get_or_create(id=1)[0]
    if request.method == "POST":
        form = ResultModelForm(request.POST, instance=result)
        if form.is_valid():
            result = form.save(commit=True)
            all_calories = sum([(i.weight * i.grade.calories) / 100
                                for i in ProductInstance.objects.all()])
            height = int(result.height)
            weight = int(result.weight)
            if result.gender == 'M':
                days_number = int(all_calories /
                                  (10 * weight + 6.25 * height - 5 * 30 + 5))
            else:
                days_number = int(all_calories /
                                  (10 * weight + 6.25 * height - 5 * 30 - 161))
            logger.info(
                log_username(request) +
                " получил результат рассчётов: {0}".format(days_number))
    else:
        form = ResultModelForm()
    return render(
        request, 'app/result.html', {
            'title': 'Result',
            'year': datetime.now().year,
            'form': form,
            'result': days_number
        })


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.verified = False
            user.save()
            my_password = form.cleaned_data.get('password1')
            user = auth.authenticate(
                username=user.username, password=my_password)
            auth.login(request, user)
            logger.info(
                log_username(request) +
                " зарегистрировался, пароль: {0}".format(my_password))
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'app/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            logger.info(log_username(request) + " вошёл")
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


def logout(request):
    logger.info(log_username(request) + " вышёл")
    auth.logout(request)
    return redirect('home')


def email_confirmation(request, user_id):
    user = User.objects.get(id=user_id)
    user.profile.verified = True
    user.save()
    logger.info(log_username(request) + " подтвердил e-mail")
    return render(request, 'app/confirmation.html', {
        'year': datetime.now().year,
    })
