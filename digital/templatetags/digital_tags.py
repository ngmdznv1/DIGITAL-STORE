from django import template
from digital.models import Category, Product, FavoriteProduct

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)

@register.simple_tag()
def get_correct_price(price, quantity=1):
    total_price = price * quantity
    return total_price

@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()

@register.simple_tag()
def get_favorites(user):
    favorites = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in favorites]
    return products