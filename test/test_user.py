from test.base import TestViewSetBase
from faker import Faker
from http import HTTPStatus

fake = Faker()


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    def generate_user_attributes(self):
        return {
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "date_of_birth": fake.date(),
            "phone": fake.phone_number(),
            "role": "developer",
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user_attributes = self.generate_user_attributes()
        user = self.create(user_attributes)

        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_update(self):
        user_attributes = self.generate_user_attributes()
        user = self.create(user_attributes)
        new_data = self.generate_user_attributes()
        updated_attributes = {**user, **new_data}

        expected_response = self.expected_details(user, updated_attributes)
        response = self.update(new_data, user["id"])
        assert response == expected_response

    def test_delete(self):
        user_attributes = self.generate_user_attributes()
        user = self.create(user_attributes)

        response = self.delete(user["id"])
        expected_response = HTTPStatus.NO_CONTENT
        assert response == expected_response

    def test_list(self):
        users_list = []
        for i in range(5):
            user_attributes = self.generate_user_attributes()
            user = self.create(user_attributes)
            users_list.append(user)

        expected_response = users_list
        response = self.list()
        response.pop(0)  # removes pytest default user
        assert response == expected_response

    def test_retrieve(self):
        users_list = []
        for i in range(5):
            user_attributes = self.generate_user_attributes()
            user = self.create(user_attributes)
            users_list.append(user)

        expected_response = users_list[2]
        response = self.retrieve(users_list[2]["id"])
        assert response == expected_response
