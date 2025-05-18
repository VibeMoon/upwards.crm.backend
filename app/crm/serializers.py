from rest_framework import serializers
from accounts.models import User, UserStatus
from accounts.serializers import UserSerializer
from .models import Project, TaskStatus, Task, UserActionStatus, UserAction, Event, AdditionalData


class AdditionalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalData
        fields = '__all__'


class AdditionalDataProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalData
        fields = ['id', 'name', 'data']


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    members = UserSerializer(many=True)
    additional_data = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Project
        fields = '__all__'

    def get_additional_data(self, obj):
        additional_data = obj.additional_data_project.all()
        if additional_data.exists():
            return AdditionalDataProjectSerializer(additional_data, many=True).data
        return []

    def get_tasks(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []

        try:
            if request.user.groups.filter(name='PM').exists():
                tasks = obj.tasks_project.all()
            else:
                tasks = obj.tasks_project.filter(assigned=request.user)

            return TaskSerializer(tasks, many=True, context=self.context).data
        except Exception:
            return []


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.EmailField(required=True)
    members = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        default=[]
    )

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_autor(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Author with this email does not exist.")
        return value

    def validate_members(self, value):
        for email in value:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    f"User with email {email} does not exist."
                )
        return value

    def create(self, validated_data):
        members_emails = validated_data.pop('members', [])
        author_email = validated_data.pop('author')

        try:
            author = User.objects.get(email=author_email)
            project = Project.objects.create(author=author, **validated_data)

            if members_emails:
                members = User.objects.filter(email__in=members_emails)
                project.members.set(members)

            return ProjectSerializer(instance=project, context=self.context).data

        except Exception as e:
            raise serializers.ValidationError(str(e))

    def update(self, instance, validated_data):
        members_emails = validated_data.pop('members', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if members_emails is not None:
            members = User.objects.filter(email__in=members_emails)
            instance.members.set(members)

        return ProjectSerializer(instance=instance, context=self.context).data


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Task
        fields = '__all__'


class UserActionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActionStatus
        fields = '__all__'


class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        fields = '__all__'


class UserActionCreateUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    user = serializers.EmailField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserAction
        fields = '__all__'

    def create(self, validated_data):
        status_slug = validated_data.pop('status')
        user_email = validated_data.pop('user')
        user = User.objects.filter(email=user_email).first()
        status = UserActionStatus.objects.filter(slug=status_slug).first()
        # if status_slug == 'come':
        #     user_status = User
        #     user.status ==
        validated_data['status'] = status
        validated_data['user'] = user
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
