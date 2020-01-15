from rest_framework import serializers
from apps.financeiro.models import Despesas
from apps.accounts.serializers import AccountSerializer
from django.conf import settings

class DespesaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesas
        fields = ("comprovante", )

class DespesasSerializer(serializers.ModelSerializer):

    solicitante = serializers.SerializerMethodField()
    comprovante = serializers.SerializerMethodField()
    # data_solicitacao = serializers.SerializerMethodField()

    class Meta:
        model = Despesas
        fields = '__all__'
    
    def get_solicitante(self, obj):
        return AccountSerializer(obj.usuario_solicitacao).data

    def get_comprovante(self, obj):
        if obj.comprovante is None:
            return None
        
        return settings.HOST + obj.comprovante.url


class NovaDespesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Despesas
        fields = ('conferencia', 'valor', 'justificativa', )
