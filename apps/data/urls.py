from django.conf import settings
from django.urls import path

from .views import DependentesApiView, DependenteApiView

urlpatterns = [
    path('dependente', DependenteApiView.as_view(), name="dependente_api"),
    path('dependentes', DependentesApiView.as_view(), name="dependentes_api"),
]
