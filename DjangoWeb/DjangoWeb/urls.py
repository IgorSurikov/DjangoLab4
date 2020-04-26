"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
admin.autodiscover()

urlpatterns = [
    path('', app.views.home, name='home'),
    path('contact/', app.views.contact, name='contact'),
    path('about/', app.views.about, name='about'),
    path('<int:product_id>/', app.views.product_grades, name ='product_grades'),
    path('<int:instance_id>/edit/', app.views.edit_product, name ='edit_product'),
    path('<int:instance_id>/delete/', app.views.delete_product, name ='delete_product'),
    path('result/', app.views.result, name ='result'),
    path('registration/',app.views.registration, name ='registration'),
    path('login/',app.views.login, name ='login'),
    path('logout/',app.views.logout, name ='logout'),
    path('admin/', admin.site.urls),
    url('confirmation/(?P<user_id>\d+)/',app.views.email_confirmation, name = 'email_confirmation')
 
]
