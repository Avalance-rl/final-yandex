from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField("Электронная почта", unique=True)
    name = models.CharField("Имя", max_length=150)
    surname = models.CharField("Фамилия", max_length=150)
    about = models.TextField("О себе", blank=True)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    github_url = models.URLField("GitHub", blank=True)
    avatar = models.FileField("Аватар", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        full_name = f"{self.name} {self.surname}".strip()
        return full_name or self.email
