from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImageItem,
    Comment,
    Tag,
    Cupon,
    CommentImage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "price",
        "available",
        "created",
        "updated",
        "rating",
        "category",
    ]
    list_filter = ["available", "created", "updated", "rating"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductImageItem)
class ProductImageItemAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class CommentImgInline(admin.TabularInline):
    model = CommentImage
    raw_id_fields = ["comment"]
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "customer", "body", "created", "updated", "active"]
    inlines = [CommentImgInline]


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ["code", "valid_from", "valid_until", "discount", "active"]
    search_fields = ["code", "discount", "active"]
    list_filter = ["active"]
