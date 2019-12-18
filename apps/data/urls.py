from django.conf import settings
from django.urls import path

from .views import DependentesApiView

urlpatterns = [
    path('dependentes', DependentesApiView.as_view(), name="dependentes_api")
]
