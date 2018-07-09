from django import template
register = template.Library()

@register.simple_tag
def get_field_label(obj, name):
    try:
        return obj._meta.get_field(name).verbose_name
    except:
        return name

@register.simple_tag
def get_field_value(obj, name):
    return getattr(obj, name)
