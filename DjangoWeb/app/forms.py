
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from app.models import ProductInstance, Result
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control'}),label = _("Логин"))
    password = forms.CharField(label=_("Пароль"),widget=forms.PasswordInput({'class': 'form-control'}))

class ProductInstanceForm(forms.Form):
    weight = forms.FloatField(label=_("Вес:"))
    grade = forms.ModelChoiceField(label = _("Cорт:"), queryset=None)
    weight.widget.attrs.update({'class':'form-control','placeholder':'граммы'})
    grade.widget.attrs.update({'class':'form-control'})

    def __init__(self, queryset, *args, **kwargs):
        super(ProductInstanceForm, self).__init__(*args, **kwargs)
        self.fields['grade'].queryset = queryset

    def clean_weight(self):
        data = self.cleaned_data['weight']
        
        if data > 100000000:
            raise ValidationError(_('Слишком большой вес'))
        return data

class ResultModelForm(forms.ModelForm):
    def clean_weight(self):
        data = self.cleaned_data['weight']

        if data < 30:
            raise ValidationError(_('Слишком маленький вес'))
        return data

    def clean_height(self):
        data = self.cleaned_data['height']

        if data < 80:
            raise ValidationError(_('Слишком маленький рост'))
        return data

    class Meta:
        model = Result
        fields = ['gender','weight','height']

        widgets = {
            'gender': forms.Select(attrs = {'class': 'form-control'}),
            'weight': forms.NumberInput(attrs = {'class': 'form-control'}),
            'height': forms.NumberInput(attrs = {'class': 'form-control'})
        }

        labels = {
            'gender': _("пол"),
            'weight': _("вес, кг"),
            'height': _("рост, см")
        }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}),label = _("Логин"))
    email = forms.EmailField(max_length=254, widget = forms.EmailInput(attrs={'class': 'form-control'}),label = _("Электронный адрес"))
    password1=forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}),label = _("Пароль"))
    password2=forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}),label = _("Подтверждение пароля"))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

       
    
