from django.conf import settings
from django.urls import path

from .views import (HomeView, inscricaoView, LoginView, NovaInscricaoView, PagarView, ContatoView, LogoutView)

urlpatterns = [
    path('', LoginView.as_view(), name="home"),
    path('dashboard', HomeView.as_view(), name="dashboard"),
    path('inscricao', inscricaoView.as_view(), name="inscricao"),
    path('nova-inscricao', NovaInscricaoView.as_view(), name="nova_inscricao"),
    path('pagar', PagarView.as_view(), name="pagar_inscricao"),
    path('contato', ContatoView.as_view(), name="contato"),
    path('logout', LogoutView.as_view(), name="logout"),
]
