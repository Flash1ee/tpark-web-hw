from django import template

register = template.Library()


@register.filter('is_newline')
def is_newline(value):
    if value % 3 == 0:
        return True
    return False


@register.filter('is_newcol_zero')
def is_newcol_zero(value):
    return value % 3 == 0

@register.filter('is_newcol_one')
def is_newcol_one(value):
    return value % 3 == 1

@register.filter('is_newcol_two')
def is_newcol_two(value):
    return value % 3 == 2