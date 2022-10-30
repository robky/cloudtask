from django.urls import path

from api.views import ConfigAPI

app_name = "api"

urlpatterns = [
    path("config", ConfigAPI.as_view()),
]
