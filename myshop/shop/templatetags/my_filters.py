from django import template
from math import floor

register = template.Library()


@register.filter(name="times")
def times(number):
    return range(number)


@register.filter(name="get_integer_part_of_number")
def get_integer_part_of_number(number):
    return floor(number)


@register.filter(name="ckek_half_star")
def ckek_half_star(number):
    if number - floor(number) > 0.2:
        return True
    return False
