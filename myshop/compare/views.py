from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from compare.compare import Compare
from shop.models import Product


def add_in_compare(request, product_id):
    product_id = int(product_id)
    product = get_object_or_404(Product, pk=product_id)
    if product:
        compare = Compare(request)
        compare.add(product_id)
        print("add", len(compare))

    return HttpResponse("Hello")
