from rest_framework import serializers

from .models import Project, Status, Task
from accounts.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=False)
    class Meta:
        model = Project
        fields = '__all__'
        ref_name = 'ProjectSerializer'


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        ref_name = 'ProjectCreateSerializer'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        ref_name = 'StatusSerializer'


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False)
    status = StatusSerializer(many=False)
    assignee = UserSerializer(many=False)

    class Meta:
        model = Task
        fields = '__all__'
        ref_name = 'TaskSerializer'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        ref_name = 'TaskCreateSerializer'