from django.conf import settings
from django.urls import path

from .views import (ConferenciaApiView, ContatoApiView, DependenteApiView,
                    DependentesApiView, InscricaoApiView,
                    InscricaoStatusPagSeguroApiView, PagamentoApiView,
                    RelatorioCidadesApiView, RelatorioHospedagemApiView,
                    RelatorioIdadesApiView, RelatorioStatusPagamentoApiView,
                    notification_view)

urlpatterns = [
    path('conferencias', ConferenciaApiView.as_view(), name="conferencias_api"),
    path('dependente', DependenteApiView.as_view(), name="dependente_api"),
    path('dependentes', DependentesApiView.as_view(), name="dependentes_api"),
    path('inscricao', InscricaoApiView.as_view(), name="inscricao_api"),
    path('contato', ContatoApiView.as_view(), name="contato_api"),
    path('pagamento', PagamentoApiView.as_view(), name="pagamento_api"),
    path('transacao_pagseguro', InscricaoStatusPagSeguroApiView.as_view(), name="transacao_pagseguro_api"),
    path('notification', notification_view, name="pagseguro_notification_api"),
    
    #relatorios
    path('relatorios/cidades', RelatorioCidadesApiView.as_view(), name="relatorio_cidades_api"),
    path('relatorios/idade', RelatorioIdadesApiView.as_view(), name="relatorio_idade_api"),
    path('relatorios/status_pagamento', RelatorioStatusPagamentoApiView.as_view(), name="relatorio_status_api"),
    path('relatorios/hospedagem', RelatorioHospedagemApiView.as_view(), name="relatorio_hospedagem_api"),
]
