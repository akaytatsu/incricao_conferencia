from django import template
from django.conf import settings
register = template.Library()

# retorna o caminho do arquivo estático seguido do timestamp representando a versão do arquivo
@register.simple_tag
def static_v(original_path):
    return settings.STATIC_URL + original_path + '?' + str(settings.VERSION)