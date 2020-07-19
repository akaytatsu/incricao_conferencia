from rest_framework import serializers

from apps.data.models import Contato, Inscricao, Dependente, Conferencia


class InscricaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inscricao
        fields = '__all__'


class InscricaoPagSeguroTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inscricao
        fields = ('pagseguro_transaction_id', 'status', )


class DependentesSerializer(serializers.ModelSerializer):

    grau_parentesco = serializers.SerializerMethodField()

    class Meta:
        model = Dependente
        fields = '__all__'
        read_only_fields = ('idade', 'valor', )

    def get_grau_parentesco(self, obj):
        return obj.grau_display()


class ContatoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Contato
        fields = ('inscricao', 'conferencia', 'nome', 'email', 'assunto', 'descricao', )


class ConferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferencia
        fields = '__all__'
