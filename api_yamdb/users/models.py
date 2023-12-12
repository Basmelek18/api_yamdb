from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole


class UserYamDb(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='роль',
        max_length=20,
        choices=UserRole.choices(),
        default=UserRole.USER
    )
    confirmation_code = models.CharField(max_length=6)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == (
            UserRole.ADMIN.value
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value

    @property
    def is_user(self):
        return self.role == UserRole.USER.value
