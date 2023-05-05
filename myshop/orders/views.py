from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Order, OrderItem


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

    return render(request, "orders/order/create.html", {"cart": cart, "form": form})
