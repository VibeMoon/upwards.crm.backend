from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class UserStatus(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус пользователя'
        verbose_name_plural = 'Статсы пользователя'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email', db_index=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', null=True, blank=True)
    avatar = models.ImageField(upload_to='user/', null=True, blank=True)
    status = models.ForeignKey(
        UserStatus, on_delete=models.SET_NULL, null=True,
        blank=True, db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField("Дата создания", auto_now_add=True)
    last_online_date = models.DateTimeField("Дата последнего входа", auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'

    def full_name(self):
        return f'{self.first_name or ""} {self.last_name or ""}'.strip()
