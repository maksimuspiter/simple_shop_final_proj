import json
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse

from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem, Status
from shop.models import Cupon
from account.models import Account


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.account
            # order.status = Status.objects.get(slug="sozdano")
            delivery_price = order.delivery.price if order.delivery else 0
            order.total_price = cart.get_total_price_with_discount() + delivery_price
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["total_price_with_discount"],
                    quantity=item["quantity"],
                )

            request.user.account.remove_cupon()
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
    discount_value = cart.get_discount_value_float()
    activated_cupon = request.user.account.activated_cupon
    return render(
        request,
        "orders/order/create.html",
        {
            "cart": cart,
            "form": form,
            "activated_cupon": activated_cupon,
            "discount_value": discount_value,
        },
    )


@require_POST
def set_coupon(request):
    coupon_code = request.POST.get("coupon_code")

    coupon = (
        Account.objects.select_related("user")
        .get(user=request.user)
        .cupons.filter(code=coupon_code, active=True)
        .first()
    )

    result = False
    error_message = None
    price_before_discount = None
    price_after_discount = None
    discount_value = None
    if coupon:
        request.user.account.activated_cupon = coupon
        request.user.account.save()
        cart = Cart(request)
        cart.add_discount(coupon.discount)
        price_before_discount, price_after_discount = cart.full_price_info_for_cart()
        discount_value = cart.get_discount_value_float()
        result = True
    else:
        error_message = "Купон не доступен"

    return HttpResponse(
        json.dumps(
            {
                "result": result,
                "error_message": error_message,
                "coupon_code": coupon_code,
                "price_before_discount": price_before_discount,
                "price_after_discount": price_after_discount,
                "discount_value": discount_value,
            }
        ),
        content_type="application/json",
    )
