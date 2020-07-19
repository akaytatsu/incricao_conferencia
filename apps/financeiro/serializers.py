from rest_framework import serializers

from apps.financeiro.models import Despesas, Comprovantes
from apps.accounts.serializers import AccountSerializer


class ComprovantesSerializer(serializers.ModelSerializer):

    comprovante = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()
    is_image = serializers.SerializerMethodField()

    class Meta:
        model = Comprovantes
        fields = "__all__"

    def get_comprovante(self, obj):
        if obj.comprovante and hasattr(obj.comprovante, 'url'):
            return obj.comprovante.url

        return None

    def get_extension(self, obj):
        url = self.get_comprovante(obj)

        if url is None:
            return None

        aux = url.split(".")

        return aux[len(aux) - 1]

    def get_is_image(self, obj):
        extension = self.get_extension(obj)

        if extension is None:
            return False

        return extension in ['jpg', 'jpeg', 'png']


class DespesaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprovantes
        fields = ("comprovante", "despesa")


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
