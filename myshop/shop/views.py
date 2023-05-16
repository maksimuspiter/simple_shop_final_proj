from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Category, Product, ProductImageItem, Tag, Comment, CommentImage
from cart.cart import Cart
from compare.compare import Compare
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DeleteView
from .forms import ReviewForm, CommentImageForm
from django.contrib.auth.decorators import login_required
from django import forms


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

        return queriset.prefetch_related("tags").select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories"] = categories
        return context


class ProductsByCategory(AllProductListView):
    def get_queryset(self, **kwargs):
        queriset = super().get_queryset()

        category_slug = self.kwargs.get("category_slug", None)

        if category_slug:
            queriset = queriset.filter(category__slug=category_slug)
        return queriset


class ProductsByTag(AllProductListView):
    def get_queryset(self, **kwargs):
        queriset = super().get_queryset()

        tag_slug = self.kwargs.get("tag_slug", None)

        if tag_slug:
            # tag = get_object_or_404(Tag, slug=tag_slug)
            queriset = queriset.filter(tags__slug=tag_slug)
        return queriset


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("tags"), id=id, slug=slug, available=True
    )
    categories = Category.objects.all()
    product_slider_img = ProductImageItem.objects.filter(product=product)
    product_comments = product.comments.all().select_related("customer__account")[:10]
    related_products = Product.objects.all().order_by("category")

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "categories": categories,
            "product_slider_img": product_slider_img,
            "product_slider_img_range": range(len(product_slider_img)),
            "related_products": related_products,
            "product_comments": product_comments,
            "product_comments_len": len(product_comments),
        },
    )


@login_required
def create_review(request, product_id):
    extra_fields = 3
    CommentImageFormSet = forms.formset_factory(CommentImageForm, extra=extra_fields)
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        form_img = CommentImageFormSet(request.POST, request.FILES)

        if form.is_valid() and form_img.is_valid():
            cd = form.cleaned_data
            imges = form_img.cleaned_data

            body = f"Достоинства: {cd['advantages']}.\nНедостатки: {cd['disadvantages']}.\nКомментарий: {cd['comment']}"
            comment = Comment.objects.create(
                product=product,
                customer=request.user,
                body=body,
                product_score=cd["product_score"],
            )
            for image in imges:
                if image.get("image"):
                    CommentImage.objects.create(comment=comment, image=image["image"])
            product.update_product_rating()
            return redirect("account:my_account")

    else:
        form = ReviewForm()
        form_img = CommentImageFormSet()

    return render(
        request,
        "shop/comment/create.html",
        {
            "form": form,
            "product": product,
            "form_img": form_img,
            "extra_fields": extra_fields,
        },
    )
