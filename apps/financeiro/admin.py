from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import CategoriaDespesa, Despesas

@admin.register(CategoriaDespesa)
class CategoriaDespesaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', )
    search_fields = ('nome', )
    list_filter = ('ativo', )


@admin.register(Despesas)
class DespesasAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'aprovado', 'comprovado', 'valor', 'categoria', 'status', 'usuario_solicitacao', 'usuario_aprovacao', 'usuario_comprovacao')
    search_fields = ('nome', )
    list_filter = ('conferencia', 'aprovado', 'comprovado', 'categoria', 'status')
