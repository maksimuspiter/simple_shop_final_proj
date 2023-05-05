from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "first_name",
        "last_name",
        "email",
        "address",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["customer", "paid", "created", "updated"]
    list_display_links = ["id", "customer"]
    inlines = [OrderItemInline]
