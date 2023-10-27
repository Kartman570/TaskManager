from factory import django, PostGenerationMethodCall, LazyAttribute, SubFactory
from faker import Faker, providers
from main.models import User, Task, Tag
from faker.providers import BaseProvider
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        file_name = f"{uuid.uuid4()}.{fmt}"
        return SimpleUploadedFile(
            file_name,
            self.generator.image(image_format=fmt),
        )


fake = Faker()
fake.add_provider(ImageFileProvider)


class UserFactory(django.DjangoModelFactory):
    avatar_picture = LazyAttribute(lambda x: fake.image_file(fmt="jpeg"))

    username = LazyAttribute(lambda x: fake.user_name())
    role = LazyAttribute(lambda x: fake.random_element(elements=User.Roles.values))
    email = LazyAttribute(lambda x: fake.email())
    first_name = LazyAttribute(lambda x: fake.first_name())
    last_name = LazyAttribute(lambda x: fake.last_name())
    date_of_birth = LazyAttribute(lambda x: fake.date())
    phone = LazyAttribute(lambda x: fake.phone_number())

    class Meta:
        model = User


class JWTFactory(UserFactory):
    password = PostGenerationMethodCall("set_password", "password")


class StaffUserFactory(UserFactory):
    is_staff = True


class TagFactory(django.DjangoModelFactory):
    name = LazyAttribute(lambda x: fake.user_name())

    class Meta:
        model = Tag


class TaskFactorySimple(django.DjangoModelFactory):
    name = fake.user_name()

    class Meta:
        model = Task


class TaskFactory(TaskFactorySimple):
    name = fake.user_name()
    description = fake.pystr()
    deadline_date = fake.future_datetime().isoformat() + "Z"
    state = "New"
    priority = 1
    author = SubFactory(UserFactory)
    worker = SubFactory(UserFactory)
    tags = SubFactory(TagFactory)

    class Meta:
        model = Task
