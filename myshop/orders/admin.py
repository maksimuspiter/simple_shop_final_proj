from django.contrib import admin
from .models import Order, OrderItem, Delivery, Status


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price"]
    list_display_links = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_display_links = ["name"]
    prepopulated_fields = {"slug": ("name",)}


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
