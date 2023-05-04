from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[("M", "Mail"), ("F", "Fimale")])
    # from shop.models import Product
    # favorite_products = models.ManyToManyField(
    #     Product, related_name="account", blank=True
    # )
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
