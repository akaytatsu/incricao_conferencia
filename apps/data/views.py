from django.contrib.auth.models import User

from apps.data.models import Contato, Dependente, Inscricao, Conferencia
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContatoSerializer, DependentesSerializer, InscricaoSerializer
from pagseguro import PagSeguro
from django.urls import reverse_lazy

from django.conf import settings


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

class PagamentoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        conferencia_pk = request.data.get("conferencia")
        inscricao_pk = request.data.get("inscricao")

        inscricao = Inscricao.objects.get(pk=inscricao_pk, conferencia_id=conferencia_pk)
        conferencia = inscricao.conferencia 

        config = { 'sandbox': False }

        pg = PagSeguro(email="iec@igrejaemcontagem.com.br", token="A30E6EFB03214526BA670F6C1ACE3EBA",)

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

        return Response({
            "code": response.code,
            "transaction": response.transaction,
            "date": response.date,
            "payment_url": response.payment_url,
            "payment_link": response.payment_link,
            "errors": response.errors,
        })
