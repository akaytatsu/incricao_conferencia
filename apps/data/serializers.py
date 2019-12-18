from rest_framework import serializers
from apps.data.models import Dependente

class DependentesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dependente
        exclude = ('idade', 'valor', )