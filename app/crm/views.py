from django.shortcuts import render
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Project, Status, Task
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer,
    StatusSerializer,
    TaskSerializer, TaskCreateSerializer
    )
from .permissions import IsAdminRole
from .repository import (
    ProjectRepository as project_model,
    TaskRepository as task_model
    )


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    filter_backends = (dj_filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title',)

    def get_queryset(self):
        return project_model.get_all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectSerializer
        elif self.request.method == 'POST':
            return ProjectCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.request.method == 'POST':
            return [IsAdminRole()]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {"detail": f"Произошла ошибка при создании проекта: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_object(self):
        project_id = self.kwargs.get('pk')
        return project_model.get_by_id(project_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        project_id = self.kwargs.get('pk')
        data = self.request.data
        project = project_model.get_by_id(project_id)
        if project:
            project_model.update(project, data)
        serializer.save()


class StatusListAPIView(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return task_model.get_all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return TaskCreateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {"detail": f"Произошла ошибка при создании таска: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task_id  = self.kwargs.get('pk')
        return task_model.get_by_id(task_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        task_id = self.kwargs.get('pk')
        data = self.request.data 
        task = task_model.get_by_id(task_id)
        if task:
            task_model.update(task, data)
        serializer.save()


class HelloView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(f'Hello {request.user.full_name()}!')
