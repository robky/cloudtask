from rest_framework import serializers

from core.models import Service, Version, Config


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ("version", )


class ConfigSerializer(serializers.ModelSerializer):
    version = VersionSerializer()

    class Meta:
        model = Config
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("service", )


class PostConfigSerializer(serializers.Serializer):
    service = serializers.CharField()
    data = serializers.ListField()

    class Meta:
        fields = ("service", "data")
