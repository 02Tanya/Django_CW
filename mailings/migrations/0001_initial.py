# Generated by Django 5.1.2 on 2024-10-19 17:40

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Без темы",
                        help_text="Укажите тему письма",
                        max_length=100,
                        verbose_name="Тема письма",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        blank=True,
                        help_text="Укажите содержание письма",
                        null=True,
                        verbose_name="Содержание письма",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите имя получателя",
                        max_length=100,
                        null=True,
                        verbose_name="Имя получателя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите фамилию получателя",
                        max_length=100,
                        null=True,
                        verbose_name="Фамилия получателя",
                    ),
                ),
                (
                    "email_address",
                    models.EmailField(
                        help_text="Введите email получателя",
                        max_length=254,
                        unique=True,
                        verbose_name="Email получателя",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Укажите комментарий",
                        max_length=300,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите владельца рассылки",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец рассылки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Адресат",
                "verbose_name_plural": "Адресаты",
                "ordering": ("last_name", "first_name", "email_address"),
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_datetime_mailing",
                    models.DateTimeField(
                        default=datetime.datetime.now,
                        help_text="Укажите дату и время старта рассылки",
                        verbose_name="Дата и время старта рассылки",
                    ),
                ),
                (
                    "stop_datetime_mailing",
                    models.DateTimeField(
                        default=datetime.datetime.now,
                        help_text="Укажите дату и время завершения рассылки",
                        verbose_name="Дата и время завершения рассылки",
                    ),
                ),
                (
                    "mailing_period",
                    models.CharField(
                        choices=[
                            ("every_day", "Ежедневно"),
                            ("every_week", "Еженедельно"),
                            ("every_month", "Ежемесячно"),
                        ],
                        default="once",
                        help_text="Укажите необходимую периодичность рассылки",
                        max_length=25,
                        verbose_name="Периодичность рассылки",
                    ),
                ),
                (
                    "mailing_status",
                    models.CharField(
                        choices=[
                            ("created", "Создана"),
                            ("started", "Запущена"),
                            ("finished", "Завершена"),
                        ],
                        default="created",
                        help_text="Укажите статус выполнения рассылки",
                        max_length=25,
                        verbose_name="Статус выполнения рассылки",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Укажите название рассылки",
                        max_length=100,
                        null=True,
                        verbose_name="Название рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Укажите активна ли рассылка",
                        verbose_name="Активная рассылка",
                    ),
                ),
                (
                    "created_date",
                    models.DateField(
                        auto_now_add=True,
                        help_text="Укажите дату создания рассылки",
                        null=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        help_text="Укажите адресатов рассылки",
                        related_name="client",
                        to="mailings.client",
                        verbose_name="Адресаты рассылки",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите владельца рассылки",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец рассылки",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите сообщение рассылки",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailings.message",
                        verbose_name="Сообщение рассылки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "permissions": [("change_activity", "Изменить aктивность рассылки")],
            },
        ),
        migrations.CreateModel(
            name="MailAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attempt_time",
                    models.DateTimeField(
                        blank=True,
                        help_text="Укажите дату и время последней попытки",
                        null=True,
                        verbose_name="Дата и время последней попытки",
                    ),
                ),
                (
                    "attempt_status",
                    models.CharField(
                        choices=[
                            ("Success", "Успешно"),
                            ("No_success", "Не осуществлена"),
                        ],
                        default="Success",
                        help_text="Укажите статус попытки",
                        max_length=15,
                        verbose_name="Статус попытки",
                    ),
                ),
                (
                    "server_response",
                    models.TextField(
                        blank=True, null=True, verbose_name="Ответ почтового сервера"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailings.client",
                        verbose_name="Клиент рассылки",
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailings.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка отправки рассылки",
                "verbose_name_plural": "Попытки отправки рассылки",
            },
        ),
    ]
