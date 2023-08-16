from rest_framework import viewsets
from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
import django_filters
from .permissions import IsStaffOrReadOnly


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.CharFilter(lookup_expr="icontains")
    worker = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ("state", "tags", "worker", "author")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by("id")
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
