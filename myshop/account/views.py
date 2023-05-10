from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Account
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, AccountEditForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from shop.models import Comment
from orders.models import Order
from cart.cart import Cart

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountDetailViewMixin(LoginRequiredMixin, DetailView):
    context_object_name = "account"

    def get_object(self):
        return get_object_or_404(
            Account.objects.prefetch_related("cupons").select_related("user__account"),
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context


class AccountDetailView(AccountDetailViewMixin):
    template_name = "account/my_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = (
            Order.objects.filter(customer=self.object)
            .select_related("customer")
            .prefetch_related("items__product")
        )
        return context


class AccountCopons(AccountDetailViewMixin):
    template_name = "account/my_copons.html"


class AccountFavoriteProducts(AccountDetailViewMixin):
    template_name = "account/my_favorite_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorite_products"] = self.object.favorite_products.all()
        context["cart_products_with_quantity"] = Cart(
            self.request
        ).get_products_with_quantity()
        return context


class AccountReviews(AccountDetailViewMixin):
    template_name = "account/my_reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["my_reviews"] = (
            Comment.objects.filter(customer=self.request.user, active=True)
            .select_related("product")
            .select_related("customer")
        )
        context["cart_products_with_quantity"] = Cart(
            self.request
        ).get_products_with_quantity()
        return context


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
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


@login_required
def edit_account(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        account_form = AccountEditForm(instance=request.user.account, data=request.POST)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect("account:my_account")

    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)

    return render(
        request,
        "account/edit_account.html",
        {"user_form": user_form, "account_form": account_form},
    )
