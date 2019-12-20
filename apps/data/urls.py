from django.conf import settings
from django.urls import path

from .views import (ConferenciaApiView, ContatoApiView, DependenteApiView,
                    DependentesApiView, InscricaoApiView,
                    InscricaoStatusPagSeguroApiView, PagamentoApiView,
                    RelatorioCidadesApiView)

urlpatterns = [
    path('conferencias', ConferenciaApiView.as_view(), name="conferencias_api"),
    path('dependente', DependenteApiView.as_view(), name="dependente_api"),
    path('dependentes', DependentesApiView.as_view(), name="dependentes_api"),
    path('inscricao', InscricaoApiView.as_view(), name="inscricao_api"),
    path('contato', ContatoApiView.as_view(), name="contato_api"),
    path('pagamento', PagamentoApiView.as_view(), name="pagamento_api"),
    path('transacao_pagseguro', InscricaoStatusPagSeguroApiView.as_view(), name="transacao_pagseguro_api"),
    
    #relatorios
    path('relatorios/cidades', RelatorioCidadesApiView.as_view(), name="relatorio_cidades_api"),
]
