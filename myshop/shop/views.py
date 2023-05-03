from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category, Product, ProductImageItem
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DeleteView


class AllProductListView(ListView):
    context_object_name = "products"
    template_name = "shop/product/list.html"

    def get_queryset(self, **kwargs):
        queriset = Product.objects.filter(available=True)

        search = self.request.GET.get("q", None)
        ordering = self.request.GET.get("order_by", "id")
        # category_slug = self.request.GET.get("category_slug",  None)
        category_slug = self.kwargs.get("category_slug", None)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queriset = queriset.filter(category=category)
        if search:
            queriset = Product.objects.filter(
                Q(name__icontains=search)
                | Q(category__name__icontains=search)
                | Q(description__icontains=search)
            )
        if ordering:
            queriset = queriset.order_by(ordering)

        return queriset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        product_ids_in_cart = Cart(self.request).get_products_ids()

        context["categories"] = categories
        context["product_ids_in_cart"] = product_ids_in_cart
        return context


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
