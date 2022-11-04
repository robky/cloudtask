from rest_framework import serializers


class DataSerializer(serializers.ListField):
    child = serializers.DictField()


class PostConfigSerializer(serializers.Serializer):
    service = serializers.CharField()
    data = DataSerializer()

    class Meta:
        fields = ("service", "data")


class PatchConfigSerializer(serializers.Serializer):
    data: dict = DataSerializer()

    class Meta:
        fields = ("data",)
