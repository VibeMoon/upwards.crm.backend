from .serializers import (
    UserActionCreateUpdateSerializer, UserActionStatusSerializer,
    ProjectSerializer, ProjectCreateUpdateSerializer, ProjectDetailSerializer,
    AdditionalDataSerializer,
    TaskStatusSerializer, TaskSerializer, TaskCreateUpdateSerializer
)
from .models import UserAction, UserActionStatus, Project, TaskStatus, Task, AdditionalData
from rest_framework import viewsets, response, status, views
from config.services import DecodeService


class UserActionStatusViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return UserActionStatus.objects.all()

    def get_serializer_class(self):
        return UserActionStatusSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserActionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return UserAction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return UserActionCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'photo' in data:
            photo_data = data.pop('photo')
            try:
                decoded_file = DecodeService.decode_file(photo_data)
                data['photo'] = decoded_file
            except Exception as e:
                return response.Response({
                    "success": False,
                    "message": f"Photo error: {str(e)}",
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data, context={'request': request})

        if not serializer.is_valid():
            return response.Response({
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return response.Response({
                "success": False,
                "message": "An error occurred during creation",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class AdditionalDataViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return AdditionalData.objects.all()

    def get_serializer_class(self):
        return AdditionalDataSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        elif self.request.method == 'GET':
            return ProjectSerializer
        elif self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return ProjectCreateUpdateSerializer


class TaskStatusViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return TaskStatus.objects.all()

    def get_serializer_class(self):
        return TaskStatusSerializer


class TaskViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Task.objects.filter(project_id=self.kwargs['project_id'])

        user = self.request.user

        if user.groups.filter(name='PM').exists():
            return queryset
        else:
            return queryset.filter(assigned=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TaskSerializer
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return TaskCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=self.kwargs['project_id'])

            request.data['project'] = project.id

            if request.user:
                request.data['author'] = request.user.id
            return super().create(request, *args, **kwargs)
        except Project.DoesNotExist:
            return response.Response(
                {"detail": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )
