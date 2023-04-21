from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=["name"],
            )
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, help_text="Имя категории")
    slug = models.SlugField(max_length=200)
    image_title = models.ImageField(upload_to="products/title/%Y/%m/%d", blank=True)
    image_slider = models.ManyToManyField("ProductImageItem", blank=True)

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена в данный момент')
    price_old = models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена до изменения')
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])


class ProductImageItem(models.Model):
    name = models.CharField(max_length=200, help_text="Имя img")
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products/slider/%Y/%m/%d", blank=True)

    class Meta:
        verbose_name = "Фото продуктов на слайдер"
        verbose_name_plural = "Фотографии продуктов на слайдер"