from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from apps.data.models import Inscricao, Conferencia
from apps.data.forms import InscricaoForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'inscricao/dashboard.html'
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conferencia'] = Conferencia.objects.get(titulo_slug=kwargs.get('conferencia'))
        
        return context


class inscricaoView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Inscricao
    template_name = 'inscricao/inscricao.html'
    form_class = InscricaoForm
    success_url = reverse_lazy('ma_produtos')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        product._cloudsearch_integrated()
        product.delete_product_cache()

        return redirect(self.success_url)

    def get_form(self, form_class=None):

        conferencia = self.get_conferencia()

        if form_class is None:
            return InscricaoForm(conferencia.pk)

        return InscricaoForm(conferencia.pk, **self.get_form_kwargs())

    def get_conferencia(self):
        slug = self.kwargs.get("conferencia")
        conferencia = Conferencia.objects.get(titulo_slug=slug)
        
        return conferencia

    def get_object(self):
        conferencia = self.get_conferencia()

        return Inscricao.objects.filter(conferencia=conferencia).first()