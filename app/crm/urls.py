from django.urls import path, include

from .views import (
    ProjectListCreateAPIView, ProjectRetrieveUpdateDestroyAPIView,
    StatusListAPIView,
    TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView,
    HelloView

)

urlpatterns = [
    path(
        'project/', ProjectListCreateAPIView.as_view(),
        name='project_list'
    ),
    path(
        'project/<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(),
        name='project_detail'
    ),
    path(
        'status/', StatusListAPIView.as_view(),
        name='status_list'
    ),
    path(
        'task/', TaskListCreateAPIView.as_view(),
        name='task_list'
    ),
    path(
        'task/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(),
        name='status_detail'
    ),
    path(
        'hello/', HelloView.as_view({'get': 'list'}),
        name='test'
    ),
]
