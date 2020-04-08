from django import template

register = template.Library()


@register.filter
def list_index(list, i):
    return list[int(i)]
