from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from apps.financeiro.models import Despesas
from apps.financeiro.serializers import DespesasSerializer, NovaDespesaSerializer

class FinanceiroViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
   
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def solicitacoes(self, request):
        if request.user.tp_user_financeiro == 0:
            return Response({}, status=200)
        
        elif request.user.tp_user_financeiro == 1:
            despesas = Despesas.objects.filter(usuario_solicitacao=request.user)
        
        else:
            despesas = Despesas.objects.all()
        
        serializer = DespesasSerializer(despesas, many=True)

        return Response(serializer.data, status=200)
   
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def nova_solicitacao(self, request):

        serializer = NovaDespesaSerializer(data=request.data) 

        if serializer.is_valid():
            obj = serializer.save(usuario_solicitacao=request.user, status=1, usuario_aprovacao=None, usuario_comprovacao=None)

            return Response(DespesasSerializer(obj).data, status=200)
        
        return Response(serializer.errors, status=400)
   
    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def aprova_solicitacao(self, request):

        pk = request.data.get("pk", None)

        if pk is None:
            return Response({"error": "Pk não informada"}, status=400)

        try:
            despesa = Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=400)

        if despesa.status != 1:
            return Response({"error": "Status atual não permite aprovação"}, status=400)

        despesa.status = 2
        despesa.save()

        return Response(DespesasSerializer(despesa).data, status=200)
   
    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def confirma_repasse_solicitacao(self, request):

        pk = request.data.get("pk", None)

        if pk is None:
            return Response({"error": "Pk não informada"}, status=400)

        try:
            despesa = Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=400)

        if despesa.status != 2:
            return Response({"error": "Status atual não permite aprovação"}, status=400)

        despesa.status = 4
        despesa.save()

        return Response(DespesasSerializer(despesa).data, status=200)
   
    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def confirma_aprovacao_solicitacao(self, request):

        pk = request.data.get("pk", None)

        if pk is None:
            return Response({"error": "Pk não informada"}, status=400)

        try:
            despesa = Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=400)

        if despesa.status != 5:
            return Response({"error": "Status atual não permite aprovação"}, status=400)

        despesa.status = 6
        despesa.save()

        return Response(DespesasSerializer(despesa).data, status=200)