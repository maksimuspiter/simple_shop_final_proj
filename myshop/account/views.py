from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account


def my_account(request):
    if request.user.is_authenticated:
        account = get_object_or_404(Account, user=request.user)
        orders = account.orders.all()
        return render(
            request, "account/my_account.html", {"account": account, "orders": orders}
        )
    return redirect("shop:product_list")
