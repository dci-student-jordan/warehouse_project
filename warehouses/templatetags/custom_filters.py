# warehouses.templatetags.custom_filters.py
from django import template
from cli.toys import glued_string

register = template.Library()

@register.filter(name='glue')
def glue(to_glue):
    return glued_string(to_glue)
    
@register.filter(name='ends_with_s')
def ends_with_s(value):
    return value[-1] == 's'