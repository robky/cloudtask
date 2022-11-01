from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils import json

from core.models import Config, Service, Version


class ConfigTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config_url = "/config"
        cls.client = APIClient()

        cls.service_name1 = "managed-k8s"
        cls.service_name2 = "mario"

        cls.data1 = [{"key1": "value1"}, {"key2": "value2"}]
        cls.data1_response = {"key1": "value1", "key2": "value2"}
        cls.data2 = [{"key1": "player1"}, {"key2": "player2"}]
        cls.data2_response = {"key1": "player1", "key2": "player2"}

        cls.config1 = {"service": cls.service_name1, "data": cls.data1}
        cls.config2 = {"service": cls.service_name2, "data": cls.data2}

        cls.service_name_url = cls.config_url + "?service=" + cls.service_name1

    def test_post_config(self):
        service_count = Service.objects.count()
        version_count = Version.objects.count()
        config_count = Config.objects.count()

        """Проверка создания сервиса"""
        response = self.client.post(self.config_url, self.config1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.config1)
        self.assertEqual(Service.objects.count(), service_count + 1)
        self.assertEqual(Version.objects.count(), version_count + 1)
        self.assertEqual(Config.objects.count(), config_count + 1)

        """Проверка создания второго сервиса"""
        response = self.client.post(self.config_url, self.config2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.config2)
        self.assertEqual(Service.objects.count(), service_count + 2)
        self.assertEqual(Version.objects.count(), version_count + 2)
        self.assertEqual(Config.objects.count(), config_count + 2)

        """Проверка добавление конфига в существующий сервис"""
        response = self.client.post(self.config_url, self.config1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.config1)
        self.assertEqual(Service.objects.count(), service_count + 2)
        self.assertEqual(Version.objects.count(), version_count + 3)
        self.assertEqual(Config.objects.count(), config_count + 3)

        """Проверка добавление конфига в существующий второй сервис"""
        response = self.client.post(self.config_url, self.config2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.config2)
        self.assertEqual(Service.objects.count(), service_count + 2)
        self.assertEqual(Version.objects.count(), version_count + 4)
        self.assertEqual(Config.objects.count(), config_count + 4)

    def test_get_config_with_service_name(self):
        """Проверка получения конфигурации по имени сервиса"""
        self.client.post(self.config_url, self.config1)
        response = self.client.get(self.service_name_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.data1_response)

    def test_update_config(self):
        """Проверка внесение изменений конфигурации в сервисе"""
        self.client.post(self.config_url, self.config1)

        response = self.client.patch(self.service_name_url, self.data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content.get("service"), self.service_name1)
        self.assertEqual(response_content.get("data"), self.data2)

        response = self.client.get(self.service_name_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_content, self.data2_response)

    def test_delete_config(self):
        service_count = Service.objects.count()
        version_count = Version.objects.count()
        config_count = Config.objects.count()

        """Проверка удаления конфигурации в сервисе"""
        self.client.post(self.config_url, self.config1)
        self.client.patch(self.service_name_url, self.data2)

        self.assertEqual(Service.objects.count(), service_count + 1)
        self.assertEqual(Version.objects.count(), version_count + 2)
        self.assertEqual(Config.objects.count(), config_count + 2)

        response = self.client.delete(self.service_name_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Service.objects.count(), service_count + 1)
        self.assertEqual(Version.objects.count(), version_count + 1)
        self.assertEqual(Config.objects.count(), config_count + 1)

        response = self.client.delete(self.service_name_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Service.objects.count(), service_count)
        self.assertEqual(Version.objects.count(), version_count)
        self.assertEqual(Config.objects.count(), config_count)
