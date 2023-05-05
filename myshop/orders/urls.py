from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("set_coupon/", views.set_coupon, name="set_coupon"),
]
