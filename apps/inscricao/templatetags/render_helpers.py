from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import math
from datetime import date
import dateutil.parser

register = template.Library()

@register.filter()
def render_errors(value):
    ret = ""
    for val in value:
        ret = ret + '<div>'
        ret = ret + '<div class="field_error">{}</div>'.format(val)
        ret = ret + '</div>'

    return mark_safe(ret)
