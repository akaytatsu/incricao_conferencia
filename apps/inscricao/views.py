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
from apps.accounts.forms import LoginForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conferencia'] = self.get_conferencia()
        
        return context

class LoginView(TemplateView):
    template_name = 'inscricao/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conferencia'] = Conferencia.objects.get(titulo_slug=kwargs.get('conferencia'))

        form = LoginForm(self.request.POST or None)  # instance= None
        context["form"] = form
        context["redirect_to"] = self.request.GET.get("redirect_to", "None")
        context["next"] = self.request.GET.get("next", "None")
        
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['not_found'] = None

        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)

                redirect_to = request.POST.get("redirect_to", "")
                next_page = request.POST.get("next", "")

                if redirect_to != "None" and redirect_to is not None and len(redirect_to) > 3:
                    return redirect(redirect_to)

                elif next_page != "None" and next_page is not None and len(next_page) > 3:
                    return redirect(next_page)

                return redirect(reverse_lazy('my_account'))
            else:
                context['not_found'] = 'Usuario não encontrado.'

        return super().render_to_response(context)
