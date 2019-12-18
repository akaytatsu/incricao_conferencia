from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from apps.data.models import Dependente

from .serializers import DependentesSerializer

class DependentesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        queryset = Dependente.objects.filter(inscricao_id=request.GET.get("inscricao_id"))
        serializer = DependentesSerializer(queryset, many=True)

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