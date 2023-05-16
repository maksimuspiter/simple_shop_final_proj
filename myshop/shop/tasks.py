from myshop.celery import app
from time import sleep
from shop.models import Product
import json


# перезапуск задачи, если во время её выполнения произошла ошибка.
@app.task(bind=True, default_retry_delay=5 * 60)
def update_product_raiting(self, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None

    if product:
        try:
            raiting = product.update_product_rating()
            result = True
        except Exception as exc:
            raise self.retry(exc=exc, countdown=60)
