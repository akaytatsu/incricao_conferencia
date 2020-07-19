from django.views.generic import TemplateView


class PregacaoView(TemplateView):
    template_name = 'pregacoes/pregacao.html'
