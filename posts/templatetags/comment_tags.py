from django import template

register = template.Library()

@register.filter
def comment_count(value):
    return len(value)

