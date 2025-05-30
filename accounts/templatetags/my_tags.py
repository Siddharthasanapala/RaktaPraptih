from django import template

register = template.Library()

@register.filter
def getattr_value(obj, attr):
    """Return the attribute of an object dynamically."""
    return getattr(obj, attr)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)