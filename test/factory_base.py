from factory import django, PostGenerationMethodCall
from faker import Faker
from main.models import User, Task


class UserFactory(django.DjangoModelFactory):
    username = Faker().user_name()
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class TaskFactory(django.DjangoModelFactory):
    name = Faker().user_name()

    class Meta:
        model = Task