from .models import Project, Task, Status
from django.db.models import Prefetch
from typing import Type, Optional
from django.db.models import Model, QuerySet

class BaseRepository:
    model: Type[Model] = None

    @classmethod
    def get_all(cls) -> QuerySet:
        return cls.model.objects.all()
    
    @classmethod
    def get_by_id(cls, obj_id: int) -> Optional[Model]:
        return cls.model.objects.filter(id=obj_id).first()
    
    @classmethod
    def create(cls, data: dict) -> Model:
        return cls.model.objects.create(**data)

    @classmethod
    def update(cls, obj: Model, data: dict) -> Model:
        for attr, value in data.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

class ProjectRepository(BaseRepository):
    model = Project

    @classmethod
    def get_all(cls):
        return cls.model.objects.prefetch_related("task").all()
    
class TaskRepository(BaseRepository):
    model = Task

    @classmethod
    def get_all(cls):
        return cls.model.objects.select_related("project", "status").all()
