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


def cart_detail(request):
    cart = Cart(request)
    # total_price = cart.get_total_price
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
