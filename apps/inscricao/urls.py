from django.conf import settings
from django.urls import path

from .views import (HomeView, inscricaoView, LoginView, NovaInscricaoView)

urlpatterns = [
    path('', LoginView.as_view(), name="home"),
    path('dashboard', HomeView.as_view(), name="dashboard"),
    path('inscricao', inscricaoView.as_view(), name="inscricao"),
    path('nova-inscricao', NovaInscricaoView.as_view(), name="nova-inscricao"),
]
