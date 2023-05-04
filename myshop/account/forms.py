from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    gender = forms.ChoiceField(
        label="Пол", widget=forms.Select(), choices=[("M", "Mail"), ("F", "Fimale")]
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Почта",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают.")
        if len(cd["password"]) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов")

        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Этот почтовый адрес уже используется.")
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["birthday", "gender"]
        widgets = {"birthday": forms.SelectDateWidget(years=range(1980, 2014))}
