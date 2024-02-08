from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import validate_username


class UserYamDb(AbstractUser):
    """Custom User Model."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class UserRole(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'
        MODERATOR = 'moderator'

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        unique=True,
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
    )
    bio = models.TextField(
        verbose_name='Biography',
        blank=True
    )
    role = models.CharField(
        verbose_name='Role',
        max_length=settings.MAX_LENGTH_ROLE,
        choices=UserRole.choices,
        default='user'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
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
