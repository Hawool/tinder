from rest_framework import serializers

from tinder.base.services import watermark
from tinder.models import Client, Match


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "username", "password", "avatar", "gender", "email",)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        avatar = watermark(validated_data['avatar'])
        client = Client.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            avatar=avatar,
            email=validated_data['email'],
        )

        return client


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
