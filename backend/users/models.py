from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.CharField(
        max_length=254,
        unique=True,
        validators=[RegexValidator(r'^\S+@\S+\.\S+$', 'Invalid email adress!')]
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+\z', 'Invalid username!')]
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    @property
    def get_full_name(self):
        """Получение полного имени пользователя."""

        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
