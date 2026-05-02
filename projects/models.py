from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    members = models.ManyToManyField(
        User,
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name