from django.conf import settings
from django.urls import path

from .views import (ContatoApiView, DependenteApiView, DependentesApiView,
                    InscricaoApiView)

urlpatterns = [
    path('dependente', DependenteApiView.as_view(), name="dependente_api"),
    path('dependentes', DependentesApiView.as_view(), name="dependentes_api"),
    path('inscricao', InscricaoApiView.as_view(), name="inscricao_api"),
    path('contato', ContatoApiView.as_view(), name="contato_api"),
]
