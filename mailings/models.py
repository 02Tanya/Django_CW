import datetime
from datetime import timezone

from django.db import models
from config import settings
from config.settings import AUTH_USER_MODEL


class Client(models.Model):
    """Клиенты сервиса рассылок - адресаты."""

    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Имя получателя",
        help_text="Введите имя получателя",
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Фамилия получателя",
        help_text="Введите фамилию получателя",
    )
    email_address = models.EmailField(
        unique=True,
        verbose_name="Email получателя",
        help_text="Введите email получателя",
    )
    comment = models.TextField(
        max_length=300,
        verbose_name="Комментарий",
        help_text="Укажите комментарий",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец рассылки",
        help_text="Укажите владельца рассылки",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email_address})"

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"
        ordering = ("last_name", "first_name", "email_address")


class Message(models.Model):
    """Сообщение, содержащееся в рассылке."""

    title = models.CharField(
        max_length=100,
        verbose_name="Тема письма",
        help_text="Укажите тему письма",
        default="Без темы",
    )
    body = models.TextField(
        verbose_name="Содержание письма",
        help_text="Укажите содержание письма",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("title",)


class Mailing(models.Model):
    """Настройки рассылки сообщений."""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    PERIOD_CHOICES = [
        ("every_day", "Ежедневно"),
        ("every_week", "Еженедельно"),
        ("every_month", "Ежемесячно"),
    ]
    start_datetime_mailing = models.DateTimeField(
        verbose_name="Дата и время старта рассылки",
        help_text="Укажите дату и время старта рассылки",
        default=datetime.datetime.now,
    )
    stop_datetime_mailing = models.DateTimeField(
        verbose_name="Дата и время завершения рассылки",
        help_text="Укажите дату и время завершения рассылки",
        default=datetime.datetime.now,
    )
    mailing_period = models.CharField(
        max_length=25,
        verbose_name="Периодичность рассылки",
        help_text="Укажите необходимую периодичность рассылки",
        choices=PERIOD_CHOICES,
        default="once",
    )
    mailing_status = models.CharField(
        max_length=25,
        verbose_name="Статус выполнения рассылки",
        help_text="Укажите статус выполнения рассылки",
        choices=STATUS_CHOICES,
        default="created",
    )

    clients = models.ManyToManyField(
        Client,
        verbose_name="Адресаты рассылки",
        help_text="Укажите адресатов рассылки",
        related_name="client",
    )
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение рассылки",
        help_text="Укажите сообщение рассылки",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название рассылки",
        help_text="Укажите название рассылки",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name="Активная рассылка",
        help_text="Укажите активна ли рассылка",
        default=True,
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания рассылки",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец рассылки",
        help_text="Укажите владельца рассылки",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.name}, Начало {self.start_datetime_mailing}, повтор {self.mailing_period}, "
            f"статус {self.mailing_status}"
        )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("change_activity", "Изменить aктивность рассылки"),
        ]


class MailAttempt(models.Model):
    """Попытки осуществления рассылки"""

    STATUS_CHOICES = [
        ("Success", "Успешно"),
        ("No_success", "Не осуществлена"),
    ]
    attempt_time = models.DateTimeField(
        verbose_name="Дата и время последней попытки",
        help_text="Укажите дату и время последней попытки",
        null=True,
        blank=True,
    )
    attempt_status = models.CharField(
        max_length=15,
        verbose_name="Статус попытки",
        help_text="Укажите статус попытки",
        choices=STATUS_CHOICES,
        default="Success",
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера", null=True, blank=True
    )

    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент рассылки",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Попытка отправки рассылки {self.attempt_time}, статус - {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка отправки рассылки"
        verbose_name_plural = "Попытки отправки рассылки"
