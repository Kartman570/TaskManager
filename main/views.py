from rest_framework import viewsets
from .models import User, Task, Tag
from .serializer import UserSerializer, TaskSerializer, TagSerializer
import django_filters


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskViewSet(viewsets.ModelViewSet):
    state = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.CharFilter(lookup_expr="icontains")
    worker = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("state", "tags", "worker", "author")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by("id")
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
