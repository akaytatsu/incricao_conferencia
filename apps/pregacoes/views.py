from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView, UpdateView

class PregacaoView(TemplateView):
    template_name = 'pregacoes/pregacao.html'
