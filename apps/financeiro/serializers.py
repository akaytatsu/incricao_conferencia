from rest_framework import serializers
from apps.financeiro.models import Despesas
from apps.accounts.serializers import AccountSerializer

class DespesasSerializer(serializers.ModelSerializer):

    solicitante = serializers.SerializerMethodField()
    # data_solicitacao = serializers.SerializerMethodField()

    class Meta:
        model = Despesas
        fields = '__all__'
    
    def get_solicitante(self, obj):
        return AccountSerializer(obj.usuario_solicitacao).data

    # def get_data_solicitacao(self, obj):
    #     return obj.data_solicitacao.strftime("%d/%m/%Y")


class NovaDespesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Despesas
        fields = ('conferencia', 'valor', 'justificativa', )
