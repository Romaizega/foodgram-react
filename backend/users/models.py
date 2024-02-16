from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.constants import MAX_EMAIL_LENGTH, MAX_FIELD_LENGTH


class FoodUser(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='Адрес электронной почты')

    username = models.CharField(
        unique=True,
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Имя пользователя',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Username может содержать только буквы, '
                         'цифры и  @/./+/-/_..')
            )
        ],
    )
    first_name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Фамилия'
    )
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        FoodUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    following = models.ForeignKey(
        FoodUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        ordering = (
            'user',
            'following')
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_user_following'
            ),
            models.CheckConstraint(
                name='ban_subscribe_to_yourself',
                check=~models.Q(user=models.F('following')),
            )
        ]

    def __str__(self):
        return f'{self.user} подписался {self.following}'
