from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Статус чата"
        verbose_name_plural = "Статусы чата"

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тип чата"
        verbose_name_plural = "Типы чата"

    def __str__(self):
        return self.name


class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="chats",
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        verbose_name="Тип чата",
    )
    status = models.ForeignKey(
        Status,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Статус чата",
        related_name="chats",
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"{self.user}: {self.type}"


class Message(models.Model):
    class Creator(models.TextChoices):
        USER = "U", "User"
        ADMIN = "A", "Admin"

    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст сообщения")
    created = models.DateTimeField(auto_now_add=True)

    creator = models.CharField(
        max_length=1,
        choices=Creator.choices,
        default=Creator.ADMIN,
        verbose_name="Автор сообщения",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.chat.user}: {self.created}"
