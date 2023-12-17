from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.v1.validators import validate_username


class UserYamDb(AbstractUser):
    """Модель кастомного пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class UserRole(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'
        MODERATOR = 'moderator'

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRole.choices,
        default='user'
    )
    confirmation_code = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name', 'first_name')

    @property
    def is_admin(self):
        return (
            self.role == self.UserRole.ADMIN.value
        ) or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR.value

    @property
    def is_user(self):
        return self.role == self.UserRole.USER.value
