from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Compare:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(settings.COMPARE_SESSION_ID)

        if not compare:
            compare = self.session[settings.COMPARE_SESSION_ID] = []

        self.compare = compare

    def __iter__(self):
        for product_id in self.compare:
            yield product_id

    def __len__(self):
        return len(self.compare)

    def add(self, product_id):
        product_id = int(product_id)

        if product_id not in self.compare:
            self.compare.append(product_id)
            self.save()
            return True

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        product_id = int(product_id)
        if product_id in self.compare:
            self.compare.remove(product_id)
            self.save()
            return True

    def clear(self):
        del self.session[settings.COMPARE_SESSION_ID]
        self.save()

    def get_all_products(self):
        return [product for product in self.compare]
