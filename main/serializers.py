from rest_framework import serializers
from .models import User
from .models import Task
from .models import Tag
from .services.file_validator import FileMaxSizeValidator
from django.core.validators import FileExtensionValidator
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ]
    )
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
            "avatar_picture",
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
