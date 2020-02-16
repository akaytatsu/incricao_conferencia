from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import (Conferencia, Contato, Dependente, Hospedagem, Inscricao,
                     Valores)

from django.utils.html import escape, mark_safe


@admin.register(Conferencia)
class ConferenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'titulo_slug', 'max_inscr', 'data_abertura', 'data_encerramento', 'inscricoes_abertas', 'pagina_inicial', )
    search_fields = ('titulo', )
    prepopulated_fields = {'titulo': ('titulo_slug',)}

    fieldsets = (
        (None, {
            'fields': ('titulo', 'titulo_slug', )
        }),
        ('Limite Conferencia', {
            'fields': ('inscricoes_abertas', 'max_inscr', 'data_abertura', 'data_encerramento',)
        }),
        ('Informações', {
            'fields': ('endereco', 'informacoes', 'informacoes_arquivo', )
        })
    )

    def pagina_inicial(self, obj):
        # link = reverse("admin:vtex_sku_changelist")
        return mark_safe('<a href="/{}/" target="_blank">{}</a>'.format(obj.titulo_slug, "Página Inicial"))

    pagina_inicial.allow_tags = True
    pagina_inicial.short_description = "Página Inicial"

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Valores)
class ValoresAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'idade_inicial', 'idade_final', 'valor', )
    search_fields = ('idade_inicial', )
    list_filter = ('conferencia', 'valor', )

@admin.register(Hospedagem)
class HospedagemAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'nome', 'limite', 'ativo', )
    search_fields = ('nome', )
    list_filter = ('conferencia', 'limite', )

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'cpf', 'nome', 'nome_cracha', 'data_nascimento', 'email', 'idade', 'cidade', 'hospedagem', 'valor', 'valor_total', 'status', 'payment_reference', 'hospedagem_detalhe', 'ver_dependentes' )
    search_fields = ('cpf', 'nome', 'email')
    list_filter = ('conferencia', 'hospedagem', 'status', 'cidade', )

    def get_readonly_fields(self, request, obj=None):

        response = []

        for f in self.model._meta.fields:
            if f.name not in [ "status", 'hospedagem', 'hospedagem_detalhe', 'data_nascimento', 'cidade']:
                response.append( f.name )

        return response

    def ver_dependentes(self, obj):
        if obj.num_dependentes() > 0:
            return mark_safe('<a href="/admin/data/dependente/?inscricao_id={}" target="_blank">ver dependente</a>'.format(obj.pk))
        else:
            return ""

    ver_dependentes.allow_tags = True
    ver_dependentes.short_description = "Ver Dependentes"

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'nome', 'nome_cracha', 'data_nascimento', 'grau', 'valor', 'hospedagem', 'hospedagem_detalhe')
    search_fields = ('inscricao__nome', 'nome', )
    list_filter = ('inscricao', 'grau', )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):

        response = []

        for f in self.model._meta.fields:
            if f.name not in ['data_nascimento', 'hospedagem', 'hospedagem_detalhe']:
                response.append( f.name )

        return response

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'inscricao', 'nome', 'email', 'data_contato',)
    search_fields = ('nome', 'email', 'descricao')
    list_filter = ('conferencia', )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
