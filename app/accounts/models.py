from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from .services import AccountsService as service

class Role(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

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
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Админ", default=False)
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
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='user/profile_photo/', null=True, blank=True, default='user/profile_photo/default_profile.jpg')

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        return self.full_name
    