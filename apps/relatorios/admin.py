from django.contrib import admin

from .models import RelatorioIdade, RelatorioCidade, RelatorioCracha, RelatorioHospedagem, RelatorioStatusPagamento


@admin.register(RelatorioCidade)
class RelatorioCidadeAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_cidade.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioCidadeAdmin, self).changelist_view(request, extra_context)


@admin.register(RelatorioIdade)
class RelatorioIdadeAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_idade.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioIdadeAdmin, self).changelist_view(request, extra_context)


@admin.register(RelatorioStatusPagamento)
class RelatorioStatusPagamentoAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_status_pagamento.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioStatusPagamentoAdmin, self).changelist_view(request, extra_context)


@admin.register(RelatorioHospedagem)
class RelatorioHospedagemAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_hospedagem.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioHospedagemAdmin, self).changelist_view(request, extra_context)


@admin.register(RelatorioCracha)
class RelatorioCrachaAdmin(admin.ModelAdmin):
    change_list_template = "relatorios/relatorio_cracha.html"

    def changelist_view(self, request, extra_context=None):
        return super(RelatorioCrachaAdmin, self).changelist_view(request, extra_context)
