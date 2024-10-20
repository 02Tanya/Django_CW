from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя пользователя",
        help_text="Введите имя пользовател]",
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия пользователя",
        help_text="Введите фамилию пользователя",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        help_text="Введите контактный номер",
        null=True,
        blank=True,
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Укажите аватар",
        null=True,
        blank=True,
    )
    token = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Token"
    )

    is_blocked = models.BooleanField(
        verbose_name="Блокировка пользователя", default=False
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Укажите комментарий",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("block_users", "Заблокuровать пользователя")]
