from rest_framework import serializers
from apps.financeiro.models import Despesas

class DespesasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Despesas
        fields = '__all__'

class NovaDespesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Despesas
        fields = ('conferencia', 'valor', 'justificativa', )




    # conferencia = models.ForeignKey(Conferencia, verbose_name="Conferencia", on_delete=models.DO_NOTHING)
    # usuario_solicitacao = models.ForeignKey(Account, verbose_name="Usuario Solicitação", related_name="usuario_solicitacao", on_delete=models.DO_NOTHING)
    # usuario_aprovacao = models.ForeignKey(Account, verbose_name="Usuario Aprovação", related_name="usuario_aprovacao", on_delete=models.DO_NOTHING)
    # usuario_comprovacao = models.ForeignKey(Account, verbose_name="Usuario Comprovação", related_name="usuario_comprovacao", on_delete=models.DO_NOTHING)
    # status = models.IntegerField(choices=_STATUS, default=1, verbose_name="Status")
    # categoria = models.ForeignKey(CategoriaDespesa, null=True, blank=True, verbose_name="Categoria de Despesa", on_delete=models.DO_NOTHING)
    # valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    # justificativa = models.CharField(max_length=500, verbose_name="Justificativa")
    # aprovado = models.BooleanField(default=False, verbose_name="Aprovado?")
    # comprovado = models.BooleanField(default=False, verbose_name="Comprovado?")