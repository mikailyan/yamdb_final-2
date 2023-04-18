from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='фамилия пользователя'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=25,
        choices=USER_ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=250,
        blank=True,
    )

    @property
    def is_admin(self):
        """Проверка на наличие прав администратора."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на наличие прав модератора."""
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        """Проверка на наличие стандартных прав."""
        return self.role == self.USER

    def __str__(self):
        return self.username
