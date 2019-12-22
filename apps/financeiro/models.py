from django.db import models
from apps.accounts.models import Account
from apps.data.models import Conferencia

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
        (3, 'Comprovação'),
    )

    conferencia = models.ForeignKey(Conferencia, verbose_name="Conferencia", on_delete=models.DO_NOTHING)
    usuario_solicitacao = models.ForeignKey(Account, verbose_name="Usuario Solicitação", related_name="usuario_solicitacao", on_delete=models.DO_NOTHING)
    usuario_aprovacao = models.ForeignKey(Account, verbose_name="Usuario Aprovação", related_name="usuario_aprovacao", on_delete=models.DO_NOTHING)
    usuario_comprovacao = models.ForeignKey(Account, verbose_name="Usuario Comprovação", related_name="usuario_comprovacao", on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=_STATUS, default=1, verbose_name="Status")
    categoria = models.ForeignKey(CategoriaDespesa, null=True, blank=True, verbose_name="Categoria de Despesa", on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    justificativa = models.CharField(max_length=500, verbose_name="Justificativa")
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado?")
    comprovado = models.BooleanField(default=False, verbose_name="Comprovado?")

    class Meta:
        db_table = "despesas"
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'