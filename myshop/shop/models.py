from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_tag", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, help_text="Имя категории")
    slug = models.SlugField(max_length=200)
    image_title = models.ImageField(upload_to="products/title/%Y/%m/%d", blank=True)
    image_slider = models.ManyToManyField("ProductImageItem", blank=True)

    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Цена в данный момент"
    )
    price_old = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Цена до изменения"
    )
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="product")

    rating = models.IntegerField(verbose_name="Рейтинг", default=0)

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


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[("M", "Mail"), ("F", "Fimale")])
    favorite_products = models.ManyToManyField(
        Product, related_name="account", blank=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"{self.user.id}: {self.user.last_name} {self.user.first_name}"


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Продукт",
    )
    customer = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="blog_comments",
        verbose_name="Автор комментария",
    )
    body = models.TextField(verbose_name="Контент", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    active = models.BooleanField(default=True, verbose_name="Активный")
    product_score = models.IntegerField(
        verbose_name="Оценка продукта",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=5,
    )

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Отзыв о товаре"
        verbose_name_plural = "Отзывы о товаре"
