from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from typing import Union, List

from main.models import User, Tag, Task
from rest_framework_simplejwt.tokens import RefreshToken
from factory_base import (
    UserFactory,
    TaskFactory,
    TagFactory,
    JWTFactory,
    StaffUserFactory,
)
from rest_framework.response import Response
from typing import Optional
import factory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    test_tag: Tag = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.api_client = APIClient()
        cls.user = cls.create_api_user()
        cls.test_tag = cls.create_test_tag()

    @classmethod
    def create_api_user(cls):
        user = factory.build(dict, FACTORY_CLASS=StaffUserFactory)
        return User.objects.create(**user)

    @classmethod
    def create_test_tag(cls):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        return Tag.objects.create(**tag_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data)
        return response

    def update(self, data: dict, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.detail_url(id), data=data)
        return response

    def delete(self, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(id))
        return response

    def list(self) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url())
        return response

    def retrieve(self, id: int = None):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(id))
        return response
