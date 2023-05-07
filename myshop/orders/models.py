from django.db import models
from shop.models import Product
from account.models import Account


class Order(models.Model):
    customer = models.ForeignKey(
        Account, related_name="orders", on_delete=models.SET_NULL, null=True
    )
    first_name = models.CharField(
        max_length=50, help_text="введите ваше имя", verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50, help_text="введите вашу фамилию", verbose_name="Фамилия"
    )
    email = models.EmailField()
    address = models.CharField(
        max_length=250, help_text="введите ваш адрес", verbose_name="адрес"
    )
    city = models.CharField(
        max_length=100, help_text="введите ваш город", verbose_name="город", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id}:: {self.email}"

    def update_total_price(self):
        self.total_price = sum(item.get_cost() for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
