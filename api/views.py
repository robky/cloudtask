from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PostConfigSerializer, ServiceSerializer
from core.models import Config, Service, Version


def new_config(data):
    serializer = PostConfigSerializer(data=data)
    if serializer.is_valid():
        service_name = serializer.validated_data.get("service")
        data = serializer.validated_data.get("data")
        if Service.objects.filter(service=service_name).exists():
            service = Service.objects.get(service=service_name)
        else:
            service = Service.objects.create(service=service_name)
        version = Version.objects.create(service=service)
        Config.objects.create(version=version, data=data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfigAPI(APIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request):
        service_name = self.request.query_params.get("service")
        if service_name:
            service = get_object_or_404(Service, service=service_name)
            last_version = service.versions.last()
            config = Config.objects.get(version=last_version)
            return Response(eval(config.data))
        else:
            queryset = Service.objects.all()
            serializer = ServiceSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        return new_config(request.data)

    def put(self, request):
        return self.post(request)

    def patch(self, request):
        service_name = self.request.query_params.get("service")
        if service_name:
            get_object_or_404(Service, service=service_name)
            config_data = request.data
            config_data = {"service": service_name, "data": config_data}
            return new_config(config_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        pass
