from rest_framework import viewsets
from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
import django_filters
from .permissions import IsPermitToDelete
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponse


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr="icontains")
    worker = django_filters.CharFilter(field_name='worker__username', lookup_expr="icontains")
    author = django_filters.CharFilter(field_name='author__username', lookup_expr="icontains")

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

#Rollbar test
def rollbar(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")