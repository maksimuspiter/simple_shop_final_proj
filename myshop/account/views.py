from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Account
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, AccountEditForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from shop.models import Cupon
from orders.models import Order
from cart.cart import Cart


@login_required
def my_account(request):
    account = get_object_or_404(
        Account.objects.prefetch_related("cupons").select_related("user"),
        user=request.user,
    )
    orders = (
        Order.objects.filter(customer=account)
        .select_related("customer")
        .prefetch_related("items__product")
    )
    cart = Cart(request)

    return render(
        request,
        "account/my_account.html",
        {"account": account, "orders": orders, "cart": cart},
    )


@login_required
def my_copons(request):
    account = get_object_or_404(
        Account.objects.prefetch_related("cupons").select_related("user"),
        user=request.user,
    )
    cart = Cart(request)

    return render(
        request,
        "account/my_copons.html",
        {"account": account, "cart": cart},
    )


@login_required
def my_favorite_products(request):
    account = get_object_or_404(
        Account.objects.select_related("user"),
        user=request.user,
    )
    favorite_products = account.favorite_products.all()
    cart = Cart(request)
    cart_products_with_quantity = get_products_with_quantity(cart)
    
    print(cart_products_with_quantity)

    return render(
        request,
        "account/my_favorite_products.html",
        {
            "account": account,
            "favorite_products": favorite_products,
            "cart": cart,
            "cart_products_with_quantity": cart_products_with_quantity,
        },
    )


def get_products_with_quantity(cart):
    product_ids_in_cart = cart.get_products_ids()
    products_with_quantity = {}
    for product_id in product_ids_in_cart:
        products_with_quantity[product_id] = cart.get_product_quantity(product_id)
    return products_with_quantity


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
