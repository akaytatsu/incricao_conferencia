from django.conf import settings
from django.urls import path

from .views import (HomeView)

urlpatterns = [
    path('dashboard', HomeView.as_view(), name="broker"),
]
