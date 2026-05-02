from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_member(self):
        return self.role == 'MEMBER'