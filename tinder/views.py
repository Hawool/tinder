from django.contrib.auth import login
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from knox.models import AuthToken
from rest_framework import permissions, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from tinder.models import Client, Match
from tinder.serializers import ClientRegisterSerializer, ClientsSerializer, MatchSerializer, ClientsDistanceSerializer


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
    serializer_class = ClientsDistanceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['gender', 'first_name', 'last_name']
    permission_classes = [permissions.IsAuthenticated]


class MatchCreateViewSet(generics.GenericAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        handpicked = Client.objects.get(id=pk)
        owner = request.user
        data = {
            'owner': owner,
            'handpicked': handpicked,
            'like': request.data['like']
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        match = serializer.save()

        handpicked_match = Match.objects.filter(owner=handpicked, handpicked=owner, like=True)

        # если симпатия от другого человека уже есть - отправка email
        if handpicked_match.exists():
            # отправка сообщения на почту (условно)
            send_mail(
                'Tinder',
                f'Вы понравились {owner.first_name} {owner.last_name}! Почта участника: {owner.email}',
                'tinder@example.com',
                [owner.email],
            )
            send_mail(
                'Tinder',
                f'Вы понравились {handpicked.first_name} {handpicked.last_name}! Почта участника: {handpicked.email}',
                'tinder@example.com',
                [handpicked.email],
            )
            return Response({'handpicked_email': handpicked.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
