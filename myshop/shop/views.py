from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Category, Product, ProductImageItem
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        "shop/product/list.html",
        # "base_products/base1.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    product_slider_img = None
    if product:
        product_slider_img = ProductImageItem.objects.filter(product=product)
    categories = Category.objects.all()

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "categories": categories,
            "product_slider_img": product_slider_img,
            "cart_product_form": cart_product_form,
            "product_slider_img_range": range(len(product_slider_img)),
        },
    )
