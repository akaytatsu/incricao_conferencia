from django.db import models
from apps.accounts.models import Account
from apps.data.models import Conferencia

class Receitas(models.Model):

    _TIPO_RECEITA = (
        (1, 'PagSeguro'),
        (2, 'Oferta'),
        (3, 'Outro'),
    )

    tipo_receita = models.IntegerField(choices=_TIPO_RECEITA, default=1, verbose_name="Tipo de Receita")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    data_receita = models.DateTimeField(auto_now_add=True, verbose_name="Data Receita", null=True)

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"


class CategoriaDespesa(models.Model):

    nome = models.CharField(max_length=80, verbose_name="Nome")
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "categoria_despesa"
        verbose_name = "Categoria Despesa"
        verbose_name_plural = "Categorias Despesa"

class Despesas(models.Model):

    _STATUS = (
        (1, 'Solicitação'),
        (2, 'Aprovada'),
        (3, 'Recurso Repassado'),
        (4, 'Aguardando Comprovação'),
        (5, 'Comprovação em Analise'),
        (6, 'Comprovado'),
    )

    conferencia = models.ForeignKey(Conferencia, verbose_name="Conferencia", on_delete=models.DO_NOTHING)
    usuario_solicitacao = models.ForeignKey(Account, verbose_name="Usuario Solicitação", related_name="usuario_solicitacao", on_delete=models.DO_NOTHING)
    usuario_aprovacao = models.ForeignKey(Account, verbose_name="Usuario Aprovação", related_name="usuario_aprovacao", on_delete=models.DO_NOTHING, null=True, blank=True)
    usuario_comprovacao = models.ForeignKey(Account, verbose_name="Usuario Comprovação", related_name="usuario_comprovacao", on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.IntegerField(choices=_STATUS, default=1, verbose_name="Status")
    categoria = models.ForeignKey(CategoriaDespesa, null=True, blank=True, verbose_name="Categoria de Despesa", on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    justificativa = models.CharField(max_length=500, verbose_name="Justificativa")
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado?")
    comprovado = models.BooleanField(default=False, verbose_name="Comprovado?")
    data_solicitacao = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Data Solicitação", )

    class Meta:
        db_table = "despesas"
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'