from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def render_errors(value):
    ret = ""
    for val in value:
        ret = ret + '<div>'
        ret = ret + '<div style="color: red">{}</div>'.format(val)
        ret = ret + '</div>'

    return mark_safe(ret)
