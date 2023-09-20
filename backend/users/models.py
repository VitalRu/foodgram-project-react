from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField('email адрес', unique=True)
    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+$', 'Invalid username!')]
    )
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    password = models.CharField('пароль', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    @property
    def get_full_name(self):
        """Получение полного имени пользователя."""

        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'auth_user'
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписавшийся пользователь',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь, на которого подписались',
        help_text='Автор',
    )

    class Meta:
        ordering = ['-author__id']
        verbose_name = 'Управление подписками'
        verbose_name_plural = 'Управление подписками'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_pair'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='author_not_user'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
