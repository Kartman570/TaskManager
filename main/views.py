from rest_framework import viewsets
from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
import django_filters
from .permissions import IsPermitToDelete
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponse
from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from typing import cast
from rest_framework_extensions.mixins import NestedViewSetMixin


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.CharFilter(field_name="tags__name", lookup_expr="icontains")
    worker = django_filters.CharFilter(
        field_name="worker__username", lookup_expr="icontains"
    )
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )

    class Meta:
        model = Task
        fields = ("state", "tags", "worker", "author")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsPermitToDelete, IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related("tags", "author", "worker").order_by("id")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsPermitToDelete, IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = [IsPermitToDelete, IsAuthenticated]


# Rollbar test
def rollbar(request):
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "worker")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()

