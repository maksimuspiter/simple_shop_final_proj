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
from account.models import Account
from .cart import Cart
from .forms import CartAddProductForm
import json


def cart_detail(request):
    cart = Cart(request)

    # for item in cart:
    #     item["update_quantity_form"] = CartAddProductForm(
    #         initial={"quantity": item["quantity"], "override": True}
    #     )
    cart_products_with_quantity = cart.get_products_with_quantity()

    account = Account.objects.prefetch_related("favorite_products").get(
        user=request.user
    )

    favorite_products = account.favorite_products.all()
    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "favorite_products": favorite_products,
            "cart_products_with_quantity": cart_products_with_quantity,
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


@require_POST
def cart_change_ajax(request):
    result = False
    quantity = None
    all_products_in_cart_quantity = None
    final_quantity_in_cart = None
    all_products_in_cart_quantity = None

    product_id = request.POST.get("product_id")
    action = request.POST.get("action")

    if product_id and action:
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

                all_products_in_cart_quantity = len(cart)

            except:
                result = False

    return HttpResponse(
        json.dumps(
            {
                "result": result,
                "final_quantity_in_cart": final_quantity_in_cart,
                "all_products_in_cart_quantity": all_products_in_cart_quantity,
            }
        ),
        content_type="application/json",
    )


@require_POST
def change_product_quantity_ajax(request):
    result = False
    quantity = None
    total_price = None
    product_total_price = None
    cart_quantity = None
    error = None

    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")

    if product_id and quantity:
        try:
            cart = Cart(request)
            product = get_object_or_404(Product, id=int(product_id))
            cart.add(product, quantity=int(quantity), override_quantity=True)
            result = True
            total_price = "%.2f" % round(cart.get_total_price(), 2)
            product_total_price = cart.get_product_sum_price_before_discount(product_id)
            cart_quantity = len(cart)

        except Exception as e:
            error = e
    return HttpResponse(
        json.dumps(
            {
                "result": result,
                "total_price": total_price,
                "product_total_price": product_total_price,
                "cart_quantity": cart_quantity,
                "error": error,
            }
        ),
        content_type="application/json",
    )
