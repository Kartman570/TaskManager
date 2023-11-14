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

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.api_client = APIClient()
        cls.user = cls.create_api_user()

    @classmethod
    def create_api_user(cls):
        user = factory.build(dict, FACTORY_CLASS=StaffUserFactory)
        return User.objects.create(**user)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=key if isinstance(key, list) else [key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create_test_user(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = User.objects.create(**user_attributes)
        return user

    def create_test_tag(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        tag = Tag.objects.create(**tag_attributes)
        return tag

    def create_test_task(self, user: User = None):
        if user is None:
            user = self.create_test_user()
        task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)
        task_attributes["author"] = user
        task_attributes["worker"] = user
        del task_attributes["tags"]
        task = Task.objects.create(**task_attributes)
        return task

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

    def list(self, data: dict = None, args: List[Union[str, int]] = None):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url(args), data=data)
        return response

    def retrieve(self, key: List[int], data: dict = None):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(key), data=data)
        return response

    def request_single_resource(self, data: dict = None) -> Response:
        self.client.force_authenticate(self.user)
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        self.client.force_authenticate(self.user)
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        self.client.force_authenticate(self.user)
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
