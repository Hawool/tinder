from rest_framework import serializers

from tinder.base.services import watermark
from tinder.models import Client, Match
from tinder.base.services import km_distance


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "username", "password", "avatar", "gender", "email", 'longitude', 'latitude')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        avatar = watermark(validated_data['avatar'])
        client = Client.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            gender=validated_data['gender'],
            avatar=avatar,
            email=validated_data['email'],
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
        )

        return client


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientsDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    distance = serializers.SerializerMethodField()

    def get_distance(self, instance):
        lon1 = self.context['request'].user.client.longitude
        lat1 = self.context['request'].user.client.latitude
        lon2 = instance.longitude
        lat2 = instance.latitude
        if lon1 and lat1 and lon2 and lat2:
            return km_distance(lon1, lat1, lon2, lat2)
        return 0.0


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
