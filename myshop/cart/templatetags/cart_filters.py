from django import template

register = template.Library()


@register.filter(name="get_renge_from_quantity")
def get_renge_from_quantity(quantity, limit, max_value=None):
    quantity, limit = int(quantity), int(limit)
    if quantity <= limit:
        return range(0, limit)

    return range(quantity - limit // 2, quantity + limit // 2)
