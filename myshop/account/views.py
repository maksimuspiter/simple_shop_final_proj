from django.db import models
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Account
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.models import User


def my_account(request):
    if request.user.is_authenticated:
        account = get_object_or_404(Account, user=request.user)
        orders = account.orders.all()
        return render(
            request, "account/my_account.html", {"account": account, "orders": orders}
        )
    return redirect("shop:product_list")


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("shop:product_list")
                else:
                    return HttpResponse("Ваш аккаунт не активен")

    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("shop:product_list")


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd["password"])
            new_user.username = f"{cd['last_name']} {cd['first_name']}"
            new_user.save()

            gender = form.cleaned_data["gender"]

            Account.objects.create(user=new_user, gender=gender)

            user = User.objects.get(email=new_user.email)

            login(request, user)
            return redirect("account:my_account")

    else:
        form = UserRegistrationForm()
    return render(request, "account/create_account.html", {"form": form})
