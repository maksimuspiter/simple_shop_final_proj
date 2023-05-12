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
        products = Product.objects.filter(id__in=self.compare)

        for product in products:
            yield product

    def __len__(self):
        print("LEN", len(self.compare))
        return len(self.compare)

    def add(self, product_id):
        product_id = int(product_id)
        print('asdds')

        if product_id not in self.compare:
            self.compare.append(product_id)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        self.compare.remove(product_id)
        self.save()

    def clear(self):
        del self.session[settings.COMPARE_SESSION_ID]
        self.save()
