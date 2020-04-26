import django
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from app.models import ProductInstance, ProductGrade


@pytest.fixture()
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DjangoDB',
        'USER': 'admin',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }


@pytest.mark.django_db
def test_home_view(client):
   url = reverse('home')
   response = client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_user_create():
  user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert user.profile.verified == False


@pytest.mark.django_db
def test_superuser(django_db_setup):
    me = User.objects.get(username='admin2')
    assert me.is_superuser


@pytest.mark.django_db
@pytest.mark.parametrize("weight,height,gender,result",
    [ ('100', '100', 'M', 20),
    ('120', '190', 'M', 13),
    ('60', '100', 'W', 33) ])
def test_result_view(weight, height, gender, result ,client):
   ProductInstance.objects.all().delete()
   ProductInstance.objects.create(weight = 10000, grade = ProductGrade.objects.get(grade_name = 'Смоленская крупа'))
   url = reverse('result')
   response = client.post(reverse('result'), {'weight': weight, 'height':height, 'gender':gender})
   assert ('<em>{0}</em>').format(str(result)).encode() in response.content


