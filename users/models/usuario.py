from django.db import models
from django.contrib.auth.models import AbstractUser
from users.enums.enum_role import RoleChoices

class User(AbstractUser):
    username = None
    email = models.EmailField()
    role = models.IntegerField(choices=RoleChoices.choices, default=RoleChoices.DIGITACION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
