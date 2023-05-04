from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
