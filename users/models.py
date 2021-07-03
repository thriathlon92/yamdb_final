from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserRole(models.TextChoices):
    admin = 'admin', 'admin'
    user = 'user', 'user'
    moderator = 'moderator', 'moderator'


class CustomUser(AbstractUser):

    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=CustomUserRole.choices,
        default=CustomUserRole.user,
    )
    email = models.EmailField(
        max_length=255, unique=True,
        blank=False, null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.role == CustomUserRole.admin or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == CustomUserRole.moderator
