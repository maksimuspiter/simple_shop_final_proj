from django.db import models
from django.contrib.auth.models import User
from shop.models import Product, Cupon


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="account",
    )
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[("M", "Mail"), ("F", "Fimale")])
    favorite_products = models.ManyToManyField(
        Product,
        related_name="account",
        verbose_name="Избранные продукты",
        blank=True,
    )
    cupons = models.ManyToManyField(
        Cupon,
        verbose_name="Доступные купоны",
        related_name="accounts",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    activated_cupon = models.ForeignKey(
        Cupon,
        verbose_name="Активированный купон",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accounts_activated",
    )

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"{self.user.id}: {self.user.last_name} {self.user.first_name}"
