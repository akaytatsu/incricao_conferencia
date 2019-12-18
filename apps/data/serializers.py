from rest_framework import serializers
from apps.data.models import Dependente

class DependentesSerializer(serializers.ModelSerializer):

    grau_parentesco = serializers.SerializerMethodField()

    class Meta:
        model = Dependente
        fields = '__all__'
        read_only_fields = ('idade', 'valor', )
    
    def get_grau_parentesco(self, obj):
        return obj.grau_display()