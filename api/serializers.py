from rest_framework import serializers

from core.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("service",)


class PostConfigSerializer(serializers.Serializer):
    service = serializers.CharField()
    data = serializers.ListField()

    class Meta:
        fields = ("service", "data")
