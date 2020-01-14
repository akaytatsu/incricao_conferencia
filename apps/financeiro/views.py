from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from apps.financeiro.models import Despesas
from apps.financeiro.serializers import DespesasSerializer, NovaDespesaSerializer, DespesaImageSerializer

class FinanceiroViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
   
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def solicitacao(self, request):
        solicitacao = Despesas.objects.get(pk=request.GET.get("id"))
        
        serializer = DespesasSerializer(solicitacao)

        return Response(serializer.data, status=200)
   
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def solicitacoes(self, request):

        solicitacoes = Despesas.objects

        if request.user.can_aprove is True:
            solicitacoes = solicitacoes
        
        elif request.user.can_pay is True:
            solicitacoes = solicitacoes.filter(status=2)

        elif request.user.can_request is True:
            solicitacoes = solicitacoes.filter(usuario_solicitacao=request.user)
        
        serializer = DespesasSerializer(solicitacoes, many=True)

        return Response(serializer.data, status=200)
   
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def nova_solicitacao(self, request):

        serializer = NovaDespesaSerializer(data=request.data) 

        if serializer.is_valid():
            obj = serializer.save(usuario_solicitacao=request.user, status=1, usuario_aprovacao=None, usuario_comprovacao=None)
            obj.notifica_nova_despesa()

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
        despesa.aprovado = True
        despesa.save()
        despesa.notifica_aprovacao()

        return Response(DespesasSerializer(despesa).data, status=200)
   
    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def reprova_solicitacao(self, request):

        pk = request.data.get("pk", None)

        if pk is None:
            return Response({"error": "Pk não informada"}, status=400)

        try:
            despesa = Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=400)

        if despesa.status != 1:
            return Response({"error": "Status atual não permite aprovação"}, status=400)

        despesa.status = 8
        despesa.save()
        despesa.notifica_reprovacao()

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
        despesa.notifica_repasse_recurso()

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
        despesa.comprovado = True
        despesa.save()
        despesa.notifica_aprovacao_comprovacao()

        return Response(DespesasSerializer(despesa).data, status=200)
   
    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def reprova_aprovacao_solicitacao(self, request):

        pk = request.data.get("pk", None)

        if pk is None:
            return Response({"error": "Pk não informada"}, status=400)

        try:
            despesa = Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=400)

        if despesa.status != 5:
            return Response({"error": "Status atual não permite aprovação"}, status=400)

        despesa.status = 4
        despesa.save()
        despesa.notifica_reprovacao_comprovacao()

        return Response(DespesasSerializer(despesa).data, status=200)
   
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def enviar_comprovante(self, request):
        despesa = Despesas.objects.get(pk=request.data.get("id"))

        serializer = DespesaImageSerializer(despesa, data=request.data, partial=True)

        if serializer.is_valid():
            obj = serializer.save()
            obj.status = 5
            obj.save()
            obj.notifica_envio_comprovacao()

            return Response({}, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)