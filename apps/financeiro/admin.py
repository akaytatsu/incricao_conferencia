from django.contrib import admin

from .models import Despesas, Receitas, Comprovantes, CategoriaDespesa


@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):

    list_display = ('tipo_receita', 'valor', 'data_receita', )
    list_filter = ('tipo_receita', )


@admin.register(CategoriaDespesa)
class CategoriaDespesaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', )
    search_fields = ('nome', )
    list_filter = ('ativo', )


@admin.register(Despesas)
class DespesasAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'aprovado', 'comprovado', 'reprovado', 'valor', 'categoria',
                    'status', 'usuario_solicitacao', 'usuario_aprovacao', 'usuario_comprovacao')
    search_fields = ('nome', )
    list_filter = ('conferencia', 'aprovado', 'comprovado', 'reprovado', 'categoria', 'status')


@admin.register(Comprovantes)
class ComprovantesAdmin(admin.ModelAdmin):
    list_display = ('despesa', 'comprovante', 'data_comprovação', )
    list_filter = ('despesa__conferencia',)
