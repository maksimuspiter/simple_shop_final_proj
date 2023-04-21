from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Category, Product, ProductImageItem
from cart.cart import Cart
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_ids_in_cart = Cart(request).get_products_ids()

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "product_ids_in_cart": product_ids_in_cart,
        },
    )


def product_detail(request, id, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = Category.objects.all()
    product_slider_img = None
    in_cart = False

    if product:
        product_slider_img = ProductImageItem.objects.filter(product=product)
        if product.id in cart.get_products_ids():
            in_cart = True
            form = CartAddProductForm(
                initial={
                    "quantity": cart.get_product_quantity(product.id),
                    "override": True,
                }
            )
        else:
            form = CartAddProductForm()

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "categories": categories,
            "product_slider_img": product_slider_img,
            "product_slider_img_range": range(len(product_slider_img)),
            "cart": cart,
            "in_cart": in_cart,
            "form": form,
        },
    )
