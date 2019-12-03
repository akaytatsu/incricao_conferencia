from django.conf import settings
from django.urls import path

from .views import (HomeView, inscricaoView)

urlpatterns = [
    path('dashboard', HomeView.as_view(), name="dashboard"),
    path('inscricao', inscricaoView.as_view(), name="inscricao"),
]
