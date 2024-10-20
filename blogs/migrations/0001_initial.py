# Generated by Django 5.1.2 on 2024-10-19 17:58

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
            name="Post",
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
                        help_text="Введите заголовок поста",
                        max_length=100,
                        verbose_name="Заголовок поста",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        help_text="Введите содержимое поста",
                        verbose_name="Содержимое поста",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Выберите изображение",
                        null=True,
                        upload_to="new_images",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now=True,
                        help_text="Укажите дату создания",
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(default=True, verbose_name="Опубликован"),
                ),
                (
                    "view_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Счётчик просмотров"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите автора",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "ordering": ("created_at",),
            },
        ),
    ]
