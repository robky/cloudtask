from django.db import models


class Service(models.Model):
    service = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.service


class Version(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.service} - {self.version}"


class Config(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        related_name="configs",
    )
    data = models.TextField()
