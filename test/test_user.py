from test.base import TestViewSetBase
from faker import Faker
from http import HTTPStatus
from test.factory_base import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile
import factory

fake = Faker()


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": "http://testserver/media/"
            + attributes["avatar_picture"].name,
        }

    def test_create(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

        user = self.create(user_attributes)

        expected_response = self.expected_details(user.data, user_attributes)
        assert user.status_code == HTTPStatus.CREATED
        assert user.data == expected_response

    def test_update(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        new_data = factory.build(dict, FACTORY_CLASS=UserFactory)
        updated_attributes = {**user.data, **new_data}

        expected_response = self.expected_details(user.data, updated_attributes)
        response = self.update(new_data, user.data["id"])

        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response

    def test_delete(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)

        response = self.delete(user.data["id"])

        assert response.status_code == HTTPStatus.NO_CONTENT
        new_response = self.retrieve(user.data["id"])
        assert new_response.status_code == HTTPStatus.NOT_FOUND

    def create_many_users(self, count: int) -> list:
        users_list = []
        for _ in range(count):
            user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
            user = self.create(user_attributes)
            users_list.append(user.data)
        return users_list

    def test_list(self):
        expected_response = self.create_many_users(5)

        response = self.list()

        response.data.pop(0)  # removes pytest default user
        assert response.data == expected_response

    def test_retrieve(self):
        users_list = self.create_many_users(5)
        expected_response = users_list[2]

        response = self.retrieve(users_list[2]["id"])

        assert response.data == expected_response

    def test_large_avatar(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"] = SimpleUploadedFile(
            "large.jpg", b"x" * 2 * 1024 * 1024
        )

        response = self.create(user_attributes)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"] = SimpleUploadedFile(
            "bad_extension.pdf", b"file_content"
        )

        response = self.create(user_attributes)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
