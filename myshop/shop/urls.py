from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path("", views.AllProductListView.as_view(), name="product_list"),
    path(
        "category/<slug:category_slug>/",
        views.ProductsByCategory.as_view(),
        name="product_list_by_category",
    ),    
    path(
        "tag/<slug:tag_slug>/",
        views.ProductsByTag.as_view(),
        name="product_list_by_tag",
    ),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("reviews/<int:product_id>/new/", views.create_review, name="create_review"),
]
