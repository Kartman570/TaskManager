from rest_framework import serializers
from .models import User
from .models import Task
from .models import Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "role",
        )


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "created_date",
            "changed_date",
            "deadline_date",
            "state",
            "priority",
            "author",
            "worker",
            "tags",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
