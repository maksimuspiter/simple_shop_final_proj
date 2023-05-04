from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import LoginForm


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

        #         else:
        #             return HttpResponse("Ваш аккаунт не активен")

    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("shop:product_list")
