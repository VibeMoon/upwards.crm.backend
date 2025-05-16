from django.db import models
from accounts.models import User


class Project(models.Model):
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authored_projects'
    )
    members = models.ManyToManyField(User, related_name='members_projects')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class AdditionalData(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    data = models.TextField()

    def __str__(self) -> str:
        return f'Project-{self.project.title}   |   data-{self.name}'


class TaskStatus(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authored_tasks'
    )
    assigned = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_tasks'
    )
    text = models.TextField()
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.text


class UserActionStatus(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.title


class UserAction(models.Model):
    status = models.ForeignKey(UserActionStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.status.title


class Event(models.Model):
    members = models.ManyToManyField(User)
    text = models.TextField()
    date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
