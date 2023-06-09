from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("change_ajax/", views.cart_change_ajax, name="cart-ajax"),
    path("change_quantity_ajax/", views.change_product_quantity_ajax, name="quantity-change-ajax"),
]
