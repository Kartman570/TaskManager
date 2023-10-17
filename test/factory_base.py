from factory import django, PostGenerationMethodCall, LazyAttribute
from faker import Faker, providers
from main.models import User, Task
from faker.providers import BaseProvider
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


fake = Faker()
fake.add_provider(ImageFileProvider)


class UserFactory(django.DjangoModelFactory):
    avatar_picture = fake.image_file(fmt="jpeg")

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


class TaskFactory(django.DjangoModelFactory):
    name = fake.user_name()

    class Meta:
        model = Task