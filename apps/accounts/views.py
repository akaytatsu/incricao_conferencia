from datetime import datetime

from django.http import Http404

from apps.accounts.models import Account
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import (FileUploadParser, FormParser, JSONParser,
                                    MultiPartParser)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountCreateSerializer, AccountSerializer


class AccountViewSet(viewsets.GenericViewSet):

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser, )

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def create_account(self, request):

        serializer = AccountCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = AccountSerializer(request.user)

        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def user_info(self, request):

        user_pk = request.data.get("user_id")

        user_pk = Account.objects.get(pk=user_pk)

        serializer = AccountSerializer(user_pk)

        return Response(serializer.data)

    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated])
    def update_onesignal_id(self, request):

        one_signal_id = request.data.get("one_signal_id")

        user = request.user
        user.onesignal_id = one_signal_id
        user.save()

        return Response({}, status=200)
