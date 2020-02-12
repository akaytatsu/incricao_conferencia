from rest_framework import serializers
from apps.financeiro.models import Despesas, Comprovantes
from apps.accounts.serializers import AccountSerializer
from django.conf import settings

class ComprovantesSerializer(serializers.ModelSerializer):

    comprovante = serializers.SerializerMethodField()
    
    class Meta:
        model = Comprovantes 
        fields = "__all__"

    def get_comprovante(self, obj):
        if obj.comprovante and hasattr(obj.comprovante, 'url'):
            return settings.HOST + obj.comprovante.url
        
        return None

class DespesaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesas
        fields = ("comprovante", )

class DespesasSerializer(serializers.ModelSerializer):

    solicitante = serializers.SerializerMethodField()
    categoria = serializers.SerializerMethodField()
    # data_solicitacao = serializers.SerializerMethodField()

    class Meta:
        model = Despesas
        fields = '__all__'
    
    def get_categoria(self, obj):
        if obj.categoria is None:
            return None
        
        return obj.categoria.nome
    
    def get_solicitante(self, obj):
        return AccountSerializer(obj.usuario_solicitacao).data


class NovaDespesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Despesas
        fields = ('conferencia', 'valor', 'justificativa', )
