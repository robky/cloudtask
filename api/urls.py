from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ConfigViewSet

app_name = "api"
router = DefaultRouter(trailing_slash=False)
router.register("config", ConfigViewSet, basename="config")

urlpatterns = [
    path("", include(router.urls)),
]
