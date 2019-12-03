from django.contrib import admin
from .models import Conferencia, Valores, Hospedagem, Inscricao, Dependente

@admin.register(Conferencia)
class ConferenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'max_inscr', 'data_abertura', 'data_encerramento', )
    search_fields = ('titulo', )

@admin.register(Valores)
class ValoresAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'idade_inicial', 'idade_final', 'valor', )
    search_fields = ('conferencia', 'idade_inicial', )
    list_filter = ('conferencia', 'valor', )

@admin.register(Hospedagem)
class HospedagemAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'nome', 'limite', 'ativo', )
    search_fields = ('conferencia', 'nome', )
    list_filter = ('conferencia', 'limite', )

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('conferencia', 'cpf', 'nome', 'nome_cracha', 'data_nascimento', 'email', 'idade', 'hospedagem', 'valor', 'valor_total', )
    search_fields = ('conferencia', 'cpf', 'nome', 'email')
    list_filter = ('conferencia', 'hospedagem', 'idade', )

@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'nome', 'nome_cracha', 'data_nascimento', 'grau', 'valor', )
    search_fields = ('inscricao', 'nome', )
    list_filter = ('inscricao', 'grau', )