from decimal import Decimal
from django.conf import settings
from shop.models import Product, Cupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["total_price_with_discount"] = item["price"] * Decimal(1 - item["discount"]/100)
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "discount": 0,
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        # пометить сессию как "измененную", чтобы убедиться, что она сохранена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_total_price_with_discount(self):
        return sum(
            Decimal(item["price"])
            * item["quantity"]
            * Decimal(1 - item["discount"] / 100)
            for item in self.cart.values()
        )

    def get_products_ids(self):
        ids = [int(id) for id in self.cart.keys()]
        return ids

    def get_product_quantity(self, product_id):
        if self.cart.get(str(product_id), None):
            return self.cart[str(product_id)]["quantity"]
        return 0

    def add_discount(self, discount: int):
        for item in self.cart.values():
            item["discount"] = discount
        self.save()
