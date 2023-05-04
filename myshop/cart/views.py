from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import json


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
        },
    )


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )

    next = request.POST.get("next")

    if next:
        return HttpResponseRedirect(next)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    next = request.POST.get("next")
    if next:
        return HttpResponseRedirect(next)
    return redirect("cart:cart_detail")


def cart_change_ajax(request, product_id):
    result = None
    quantity = None

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            quantity = 1
        elif action == "remove":
            quantity = -1

    if quantity:
        try:
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)

            result = True
            quantity_in_cart = cart.get_product_quantity(product_id)

            final_quantity_in_cart = quantity_in_cart + quantity
            if final_quantity_in_cart > 0:
                cart.add(product=product, quantity=quantity)
            elif final_quantity_in_cart == 0:
                cart.remove(product)

            elif final_quantity_in_cart < 0:
                result = False
                final_quantity_in_cart = 0

        except:
            result = False

    return HttpResponse(
        json.dumps(
            {"result": result, "final_quantity_in_cart": final_quantity_in_cart}
        ),
        content_type="application/json",
    )
