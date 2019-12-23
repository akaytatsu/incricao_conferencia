from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Count
from django.urls import reverse_lazy

from apps.data.models import Conferencia, Contato, Dependente, Inscricao
from pagseguro import PagSeguro
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ConferenciaSerializer, ContatoSerializer,
                          DependentesSerializer,
                          InscricaoPagSeguroTransactionSerializer,
                          InscricaoSerializer)


class DependentesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        queryset = Dependente.objects.filter(inscricao_id=request.GET.get("inscricao_id"))
        queryset = queryset.order_by('-idade')
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
            dependente = serializer.save()
            inscricao = dependente.inscricao
            inscricao.atualiza_valor_total()

            return Response( serializer.data, status=200 )

        return Response(serializer.errors, status=400)

    def delete(self, request, format=None):

        try:
            dependente = Dependente.objects.get(id=request.GET.get("id"), inscricao_id=request.GET.get("inscricao"))
        except Dependente.DoesNotExist:
            return Response({}, status=400)

        inscricao = dependente.inscricao
        inscricao.atualiza_valor_total()
        dependente.delete()

        return Response({}, status=200 )

class ConferenciaApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Conferencia.objects.all()
        serializer = ConferenciaSerializer(queryset, many=True)

        return Response(serializer.data)

class InscricaoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        queryset = Inscricao.objects.get(id=request.GET.get("inscricao_id"), data_nascimento=self.request.user.data_nascimento)
        
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

class InscricaoStatusPagSeguroApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        data = request.data.copy()

        inscricao = Inscricao.objects.get(pk=data['inscricao'])
        conferencia = Conferencia.objects.get(pk=data['conferencia'])

        data['inscricao'] = inscricao.pk
        data['conferencia'] = conferencia.pk

        serializer = InscricaoPagSeguroTransactionSerializer(inscricao, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=200)

        return Response(serializer.errors, status=400)

class PagamentoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        conferencia_pk = request.data.get("conferencia")
        inscricao_pk = request.data.get("inscricao")

        inscricao = Inscricao.objects.get(pk=inscricao_pk, conferencia_id=conferencia_pk)
        conferencia = inscricao.conferencia  

        config = { 'sandbox': False }

        pg = PagSeguro(email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,)

        pg.sender = {
            "name": inscricao.nome,
            "area_code": inscricao.ddd,
            "phone": inscricao.cleanned_telefone(),
            "email": inscricao.email,
        }

        pg.shipping = {
            "type": pg.NONE,
            "street": inscricao.endereco,
            "number": inscricao.numero,
            "complement": inscricao.complemento,
            "district": inscricao.bairro,
            "postal_code": inscricao.cep,
            "city": inscricao.cidade,
            "state": inscricao.uf,
            "country": "BRA"
        }

        pg.reference_prefix = "REFID_"
        pg.reference = inscricao.pk

        pg.items = [
            {
                "id": "0001", 
                "description": conferencia.titulo, 
                "amount": inscricao.valor_total, 
                "quantity": 1,
            },
        ]

        url_base = reverse_lazy('home', kwargs={"conferencia": conferencia.titulo_slug})

        redirect_url = "{}{}".format(settings.BASE_URL, url_base)

        pg.redirect_url = redirect_url
        pg.notification_url = settings.NOTIFICATION_URL

        response = pg.checkout()

        inscricao.payment_reference = pg.reference
        inscricao.status = 1
        inscricao.save()

        return Response({
            "code": response.code,
            "transaction": response.transaction,
            "date": response.date,
            "payment_url": response.payment_url,
            "payment_link": response.payment_link,
            "errors": response.errors,
            "pre_ref": pg.reference_prefix,
            "reference": pg.reference,
        })

def notification_view(request):
    notification_code = request.POST['notificationCode']
    pg = PagSeguro(email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,)
    notification_data = pg.check_notification(notification_code)

    inscricao = Inscricao.objects.get(payment_reference=notification_data.get("reference"))
    
    inscricao.sit_pagseguro = notification_data.get("status")

    if notification_data.get("status") == 3:
        inscricao.status = 2
    
    inscricao.save()

    return Response({}, status=200)


################
## RELATORIOS
################

def sortByQuantity(e):
    return e['inscricao__count'] + e['dependentes__count']

class RelatorioCidadesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        querystr = """
            select
                1 as id,
                i.cidade,
                ( (select count(*) from dependente dep join inscricao subi on subi.id = dep.inscricao_id where subi.cidade = i.cidade) ) dependentes__count,
                ( select count(*) from inscricao subi where subi.cidade = i.cidade  ) inscricao__count
            from
                inscricao i
            where
                i.conferencia_id = {}
            group by
                i.cidade
        """.format(request.data.get("conferencia_id"))

        queryset = Inscricao.objects.raw(querystr)

        response = []

        for data in queryset:
            response.append({
                "cidade": data.cidade,
                "dependentes__count": data.dependentes__count,
                "inscricao__count": data.inscricao__count,
            })

        response.sort(reverse=True, key=sortByQuantity)

        return Response(response)
