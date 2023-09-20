from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from typing import Union, List

from main.models import User, Tag
from rest_framework_simplejwt.tokens import RefreshToken

class TestViewSetBase(APITestCase):
    user_attributes = {}
    user: User = None
    client: APIClient = None
    tag_attributes = {}
    tag: Tag = None
    basename: str
    JWT_token = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user, cls.JWT_token = cls.create_api_user()
        cls.user.is_staff = True
        cls.user.save()
        cls.client = APIClient()

    @classmethod
    def create_api_user(cls):
        user = User.objects.create(**cls.user_attributes)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return user, access_token

    @classmethod
    def create_test_tag(cls):
        return Tag.objects.create(**cls.tag_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.JWT_token}')
        response = self.client.post(self.list_url(args), data=data)
        return response

    def update(self, data: dict, id: int = None) -> dict:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.JWT_token}')
        response = self.client.patch(self.detail_url(id), data=data)
        return response

    def delete(self, id: int = None) -> dict:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.JWT_token}')
        response = self.client.delete(self.detail_url(id))
        return response

    def list(self) -> dict:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.JWT_token}')
        response = self.client.get(self.list_url())
        return response

    def retrieve(self, id: int = None):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.JWT_token}')
        response = self.client.get(self.detail_url(id))
        return response
