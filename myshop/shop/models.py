from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["slug"]
        indexes = [
            models.Index(
                fields=["slug"],
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
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["slug"]
        indexes = [
            models.Index(
                fields=["slug"],
            )
        ]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

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
    rating = models.FloatField(verbose_name="Рейтинг", default=0)

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

    def update_product_rating(self):
        self.rating = self.comments.all().aggregate(Avg("product_score"))[
            "product_score__avg"
        ]
        self.save()
        return self.rating


class ProductImageItem(models.Model):
    name = models.CharField(max_length=200, help_text="Имя img")
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products/slider/%Y/%m/%d", blank=True)

    class Meta:
        verbose_name = "Фото продуктов на слайдер"
        verbose_name_plural = "Фотографии продуктов на слайдер"


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Продукт",
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
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


class CommentImage(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Комментарий",
    )
    image = models.ImageField(
        upload_to="comment_img/%Y/%m/%d", blank=True, verbose_name="Фото"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
            models.Index(fields=["comment"]),
        ]
        verbose_name = "Отзыв о товаре"
        verbose_name_plural = "Отзывы о товаре"


class Cupon(models.Model):
    code = models.CharField(max_length=50, help_text="Код Купона", unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    valid_from = models.DateTimeField(
        blank=True, null=True, help_text="Действителен с этой даты"
    )
    valid_until = models.DateTimeField(
        blank=True, null=True, help_text="Действителен до этой даты"
    )
    discount = models.IntegerField(
        verbose_name="Процент скидки",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return self.code

    def check_active(self):
        now = timezone.now()
        self.active = self.valid_from >= now and self.valid_until <= now
        self.save()
