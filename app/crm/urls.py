from django.urls import path
from .views import (
    UserActionViewSet, UserActionStatusViewSet,
    AdditionalDataViewSet,
    ProjectViewSet,
    TaskStatusViewSet, TaskViewSet
)

urlpatterns = [
    path(
        'user-actions/',
        UserActionViewSet.as_view({"get": "list", "post": "create"}),
        name='user_event'
    ),
    path(
        'user-action-statuses/',
        UserActionStatusViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        'additional-data/',
        AdditionalDataViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        'projects/',
        ProjectViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        'projects/<int:pk>',
        ProjectViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})
    ),
    path(
        'tasks-status/',
        TaskStatusViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        'tasks/<int:project_id>/',
        TaskViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        'tasks/<int:pk>/',
        TaskViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})
    )
]
