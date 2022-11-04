from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PatchConfigSerializer, PostConfigSerializer
from core.models import Config, Service, Version

service_name = openapi.Parameter(
    "service",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="Укажите имя приложения",
    required=True,
)


def new_config(data):
    serializer = PostConfigSerializer(data=data)
    if serializer.is_valid():
        service_value = serializer.validated_data.get("service")
        data = serializer.validated_data.get("data")
        config_data = {}
        [config_data.update(value) for value in data]
        if Service.objects.filter(service=service_value).exists():
            service = Service.objects.get(service=service_value)
        else:
            service = Service.objects.create(service=service_value)
        version = Version.objects.create(service=service)
        Config.objects.create(version=version, data=config_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfigAPI(APIView):
    # serializer_class = PostConfigSerializer

    @swagger_auto_schema(
        operation_summary="Получить конфигурацию приложения.",
        operation_description="Получить последнюю версию конфигурации "
        "указанного (service) приложения.",
        manual_parameters=[service_name],
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Конфигурация {string: string}"
            ),
            status.HTTP_404_NOT_FOUND: "Not found",
        },
    )
    def get(self, request):
        service_value = self.request.query_params.get("service")
        if not service_value:
            return Response(status=status.HTTP_404_NOT_FOUND)
        service = get_object_or_404(Service, service=service_value)
        last_version = service.versions.last()
        config = Config.objects.get(version=last_version)
        return Response(eval(config.data))

    @swagger_auto_schema(
        operation_summary="Записать конфигурацию приложения",
        operation_description="Записать конфигурацию приложения (service). "
        "Если приложение существует, то запишется новая версия.",
        request_body=PostConfigSerializer,
    )
    def post(self, request):
        return new_config(request.data)

    @swagger_auto_schema(
        operation_summary="Записать новую версию конфигурации приложения",
        operation_description="Записать новую версию конфигурацию приложения "
        " (service). Эквивалентно POST.",
        request_body=PostConfigSerializer,
        responses={
            status.HTTP_201_CREATED: PostConfigSerializer,
        },
    )
    def put(self, request):
        return self.post(request)

    @swagger_auto_schema(
        operation_summary="Изменить конфигурацию приложения",
        operation_description="Записать измененную версию конфигурации "
        "указанного приложения (service).",
        manual_parameters=[service_name],
        request_body=PatchConfigSerializer,
        responses={
            status.HTTP_201_CREATED: PostConfigSerializer,
            status.HTTP_404_NOT_FOUND: "Not found",
        },
    )
    def patch(self, request):
        serializer = PatchConfigSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        service_value = self.request.query_params.get("service")
        if not service_value:
            return Response(status=status.HTTP_404_NOT_FOUND)
        service = get_object_or_404(Service, service=service_value)
        last_version = service.versions.last()
        config = Config.objects.get(version=last_version)
        config_data = {"service": service_value}
        temp = eval(config.data)
        patch_data = request.data.get("data")
        [temp.update(value) for value in patch_data]
        config_data["data"] = [temp]
        return new_config(config_data)

    @swagger_auto_schema(
        operation_summary="Удалить конфигурацию",
        operation_description="Удалить последнюю версию конфигурации "
        "приложения (service). Если существуют одна версия конфигурации, то"
        "будет удалено и конфигурация и приложение",
        manual_parameters=[service_name],
        responses={
            status.HTTP_204_NO_CONTENT: "Deleted",
            status.HTTP_404_NOT_FOUND: "Not found",
        },
    )
    def delete(self, request):
        service_value = self.request.query_params.get("service")
        if not service_value:
            return Response(status=status.HTTP_404_NOT_FOUND)
        service = get_object_or_404(Service, service=service_value)
        if service.versions.all().count() > 1:
            last_version = service.versions.last()
            last_version.delete()
        else:
            service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
