from rest_framework import serializers

from .models import Account
from django.conf import settings

class AccountCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=80, required=True)
    telefone = serializers.CharField(max_length=120, required=True)

    def create(self, validated_data):

        user = Account.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            telefone=validated_data['telefone'],
            can_request=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        if not data.get('password') or not data.get('password_confirm'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Those passwords don't match.")

        try:
            Account.objects.get(email=data.get('email'))
            raise serializers.ValidationError("Email already exists.")
        except Account.DoesNotExist:
            pass

        return data

    class Meta:
        model = Account
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "name", "password", "password_confirm", "email", 'telefone', )

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "email", "telefone", "can_request", "can_aprove", "can_pay", "tp_user_financeiro")
