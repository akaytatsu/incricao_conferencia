from django.urls import path

from .views import PregacaoView

urlpatterns = [
    path('sermon', PregacaoView.as_view(), name="pregacao"),
]
