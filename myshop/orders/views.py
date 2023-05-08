from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Order, OrderItem
from account.models import Account
from shop.models import Cupon
from django.views.decorators.http import require_POST
import json


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.account
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            return redirect(reverse("cart:cart_detail"))

    else:
        form = OrderCreateForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

    activated_cupon = request.user.account.activated_cupon
    return render(
        request,
        "orders/order/create.html",
        {"cart": cart, "form": form, "activated_cupon": activated_cupon},
    )


@require_POST
def set_coupon(request):
    coupon_code = request.POST.get("coupon_code")
    coupon = Cupon.objects.filter(code=coupon_code, active=True).first()
    result = False
    price_before_discount = None
    price_after_discount = None
    if coupon:
        request.user.account.activated_cupon = coupon
        request.user.account.save()
        cart = Cart(request)
        cart.add_discount(coupon.discount)
        price_before_discount = "%.2f" % round(cart.get_total_price(), 2)
        price_after_discount = "%.2f" % round(cart.get_total_price_with_discount(), 2)
        result = True

    return HttpResponse(
        json.dumps(
            {
                "result": result,
                "coupon_code": coupon_code,
                "price_before_discount": price_before_discount,
                "price_after_discount": price_after_discount,
            }
        ),
        content_type="application/json",
    )
