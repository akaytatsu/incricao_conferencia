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
        (8, 'Reprovado'),
    )

    conferencia = models.ForeignKey(Conferencia, verbose_name="Conferencia", on_delete=models.DO_NOTHING)
    usuario_solicitacao = models.ForeignKey(Account, verbose_name="Usuario Solicitação", related_name="usuario_solicitacao", on_delete=models.DO_NOTHING)
    usuario_aprovacao = models.ForeignKey(Account, verbose_name="Usuario Aprovação", related_name="usuario_aprovacao", on_delete=models.DO_NOTHING, null=True, blank=True)
    usuario_comprovacao = models.ForeignKey(Account, verbose_name="Usuario Comprovação", related_name="usuario_comprovacao", on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.IntegerField(choices=_STATUS, default=1, verbose_name="Status")
    categoria = models.ForeignKey(CategoriaDespesa, null=True, blank=True, verbose_name="Categoria de Despesa", on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    justificativa = models.CharField(max_length=500, verbose_name="Justificativa")
    justificativa_reprovacao = models.CharField(max_length=500, verbose_name="Justificativa Reprovação", null=True, blank=True)
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado?")
    comprovado = models.BooleanField(default=False, verbose_name="Comprovado?")
    reprovado = models.BooleanField(default=False, verbose_name="Reprovado?")
    data_solicitacao = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Data Solicitação", )

    class Meta:
        db_table = "despesas"
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
    
    def notifica_nova_despesa(self):

        accounts = Account.objects.filter(can_aprove=True)

        onesignal_ids = [ac.onesignal_id for ac in accounts]

        titulo = "Nova solicitação de recurso"
        mensagem = "{} solicitou R$ {}".format(self.usuario_solicitacao.name, self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})
    
    def notifica_aprovacao(self):
        # Notifica solicitante
        onesignal_ids = [self.usuario_solicitacao.onesignal_id]

        titulo = "Solicitação de recurso Aprovada"
        mensagem = "Sua solicitação de R$ {} foi aprovada".format(self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})

        accounts = Account.objects.filter(can_pay=True)

        onesignal_ids = [ac.onesignal_id for ac in accounts]

        titulo = "Repasse de recurso pendente"
        mensagem = "A solicitação de R$ {} para {} foi aprovada. Pendente o repasse do recurso".format(self.valor, self.usuario_solicitacao.name)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})
    
    def notifica_reprovacao(self):
        # Notifica solicitante
        onesignal_ids = [self.usuario_solicitacao.onesignal_id]

        titulo = "Solicitação de recurso Reprovada"
        mensagem = "Sua solicitação de R$ {} foi reprovada".format(self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})
    
    def notifica_repasse_recurso(self):

        # Notifica solicitante
        onesignal_ids = [self.usuario_solicitacao.onesignal_id]

        titulo = "Recurso repassado"
        mensagem = "O recurso referente a solicitação de R$ {} foi repassado".format(self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})

        accounts = Account.objects.filter(can_aprove=True)

        onesignal_ids = [ac.onesignal_id for ac in accounts]

        titulo = "Repasse de recurso excutado"
        mensagem = "O recurso de R$ {} para {} foi repassado.".format(self.valor, self.usuario_solicitacao.name)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})
    
    def notifica_envio_comprovacao(self):
        accounts = Account.objects.filter(can_aprove=True)

        onesignal_ids = [ac.onesignal_id for ac in accounts]

        titulo = "Envio de Comprovação"
        mensagem = "{} envio comprovação referente ao valor de R$ {}.".format(self.usuario_solicitacao.name, self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})

    def notifica_aprovacao_comprovacao(self):

        # Notifica solicitante
        onesignal_ids = [self.usuario_solicitacao.onesignal_id]

        titulo = "Comprovação aprovada"
        mensagem = "Sua comprovação referente a solicitação de R$ {} foi aprovada".format(self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})

    def notifica_reprovacao_comprovacao(self):

        # Notifica solicitante
        onesignal_ids = [self.usuario_solicitacao.onesignal_id]

        titulo = "Comprovação com pendencias"
        mensagem = "Sua comprovação referente a solicitação de R$ {} foi reprovada. Por favor verifique.".format(self.valor)

        response = Account.notificate(titulo, mensagem, onesignal_ids, params={"id": self.id})


class Comprovantes(models.Model):

    despesa = models.ForeignKey(Despesas, verbose_name="Despesa", on_delete=models.DO_NOTHING)
    comprovante = models.ImageField(upload_to='comprovantes/', null=True, blank=True)
    data_comprovação = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Data Comprovação", )

    class Meta:
        db_table = "comprovantes_despesa"
        verbose_name = "Comprovante Despesa"
        verbose_name_plural = "Comprovantes Despesa"