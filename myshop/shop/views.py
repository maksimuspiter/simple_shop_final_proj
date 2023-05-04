from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category, Product, ProductImageItem, Tag
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


class ProductsByCategory(AllProductListView):
    def get_queryset(self, **kwargs):
        queriset = super().get_queryset()

        category_slug = self.kwargs.get("category_slug", None)

        if category_slug:
            queriset = (
                queriset.filter(category__slug=category_slug)
                .select_related("category")
                .prefetch_related("tags")
            )
        return queriset


class ProductsByTag(AllProductListView):
    def get_queryset(self, **kwargs):
        queriset = super().get_queryset()

        tag_slug = self.kwargs.get("tag_slug", None)

        if tag_slug:
            # tag = get_object_or_404(Tag, slug=tag_slug)
            queriset = (
                queriset.filter(tags__slug=tag_slug)
                .select_related("category")
                .prefetch_related("tags")
            )
        return queriset


def product_detail(request, id, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = Category.objects.all()

    product_slider_img = ProductImageItem.objects.filter(product=product)
    products_in_cart_quantity = cart.get_product_quantity(product.id)

    # related_products = Product.objects.filter(available=True, category=product.category)
    product_comments = product.comments.all()[:10]
    related_products = Product.objects.all().order_by("category")

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "categories": categories,
            "product_slider_img": product_slider_img,
            "product_slider_img_range": range(len(product_slider_img)),
            "cart": cart,
            "products_in_cart_quantity": products_in_cart_quantity,
            "related_products": related_products,
            "product_comments": product_comments,
        },
    )


def my_account(request):
    return render(request, "shop/account/my_account.html")
