from django.db.models import Prefetch

from .models import Project, Task, Status
from config.base_repository import BaseRepository

class ProjectRepository(BaseRepository):
    """
    Это репозиторий для работы с моделю Project
    """
    model = Project
    
class TaskRepository(BaseRepository):
    """
    Это репозиторий для работы с моделью Task
    """
    model = Task

    @classmethod
    def get_all(cls):
        """
        Получает все задачи (Task) из базы данных с предзагрузкой связанных объектов
        """
        return cls.model.objects.select_related("project", "status").all()
