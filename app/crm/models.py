from django.db import models
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

User = get_user_model()


class Project(models.Model):
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=255)
    design_reference = models.TextField(null=True)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус таск'
        verbose_name_plural = 'Статусы таск'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = RichTextField(null=True)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Таск'
        verbose_name_plural = 'Таски'
