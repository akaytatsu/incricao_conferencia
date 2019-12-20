from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import RelatorioCidade


@admin.register(RelatorioCidade)
class RelatorioCidadeAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_cidade.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioCidadeAdmin, self).changelist_view(request, extra_context)
