from django.urls import path

from .views import (
    HomeView, LoginView, PagarView, LogoutView, ContatoView, DependentesView, NovaInscricaoView, inscricaoView
)

urlpatterns = [
    path('', LoginView.as_view(), name="home"),
    path('dashboard', HomeView.as_view(), name="dashboard"),
    path('inscricao', inscricaoView.as_view(), name="inscricao"),
    path('dependentes', DependentesView.as_view(), name="dependentes"),
    path('nova-inscricao', NovaInscricaoView.as_view(), name="nova_inscricao"),
    path('pagar', PagarView.as_view(), name="pagar_inscricao"),
    path('contato', ContatoView.as_view(), name="contato"),
    path('logout', LogoutView.as_view(), name="logout"),
]
