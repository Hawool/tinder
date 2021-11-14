from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from tinder.models import Client
from tinder.serializers import ClientRegisterSerializer, ClientsSerializer


class CreateClientView(generics.GenericAPIView):
    # model = Client
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return Response({
            "user": ClientsSerializer(client, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(client)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.validated_data['user']
        login(request, client)
        return super(LoginAPI, self).post(request, format=None)


class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientsSerializer
    # permission_classes = [permissions.IsAuthenticated]
