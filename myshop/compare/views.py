from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from compare.compare import Compare
from shop.models import Product
from django.views.decorators.http import require_POST
import json
from django.views.generic import ListView

@require_POST
def in_compare(request):
    product_id = request.POST.get("product_id")
    product_id = int(product_id)
    error = None
    result = None
    action = None
    compare_len = None
    product = get_object_or_404(Product, pk=product_id)
    if product:
        compare = Compare(request)
        if product_id in compare:
            compare.remove(product_id)
            action = "remove"
        else:
            compare.add(product_id)
            action = "add"

        result = True
        compare_len = len(compare)

    return HttpResponse(
        json.dumps(
            {
                "result": result,
                "compare_len": compare_len,
                "error": error,
                "action": action,
            }
        ),
        content_type="application/json",
    )

class ListOfComparesListView(ListView):
    context_object_name = "products"
    template_name = "compare/list_of_compare.html"

    def get_queryset(self, **kwargs):
        compare = Compare(self.request)
        queriset = Product.objects.filter(id__in=compare.get_all_products()).prefetch_related("tags").select_related("category")
        return queriset