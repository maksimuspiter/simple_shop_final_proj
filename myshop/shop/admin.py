from django.contrib import admin
from .models import Category, Product, ProductImageItem, Account, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductImageItem)
class ProductImageItemAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["user", "birthday", "gender", "created", "updated"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "author", "body", "created", "updated", "active"]
