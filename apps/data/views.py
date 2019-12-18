from django.contrib.auth.models import User

from apps.data.models import Contato, Dependente, Inscricao, Conferencia
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContatoSerializer, DependentesSerializer, InscricaoSerializer


class DependentesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        queryset = Dependente.objects.filter(inscricao_id=request.GET.get("inscricao_id"))
        serializer = DependentesSerializer(queryset, many=True)

        return Response(serializer.data)

class DependenteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Dependente.objects.get(id=request.GET.get("id"), inscricao_id=request.GET.get("inscricao_id"))
        serializer = DependentesSerializer(queryset)

        return Response(serializer.data)

    def post(self, request, format=None):

        if request.data.get("id") is None or request.data.get("id") == "":
            serializer = DependentesSerializer( data=request.data )
        else:
            queryset = Dependente.objects.get(id=request.data.get("id"))
            serializer = DependentesSerializer( queryset, data=request.data )

        
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=200 )

        return Response(serializer.errors, status=400)

    def delete(self, request, format=None):

        try:
            dependente = Dependente.objects.get(id=request.GET.get("id"), inscricao_id=request.GET.get("inscricao"))
        except Dependente.DoesNotExist:
            return Response({}, status=400)

        dependente.delete()

        return Response({}, status=200 )

class InscricaoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        queryset = Inscricao.objects.get(id=request.GET.get("inscricao_id"), cpf=self.request.user.cpf, data_nascimento=self.request.user.data_nascimento)
        
        serializer = InscricaoSerializer(queryset)

        return Response(serializer.data)

class ContatoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        data = request.data.copy()
        data['inscricao'] = Inscricao.objects.get(pk=data['inscricao']).pk
        data['conferencia'] = Conferencia.objects.get(pk=data['conferencia']).pk

        serializer = ContatoSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=200)

        return Response(serializer.errors, status=400)
