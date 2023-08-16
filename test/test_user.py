from test.base import TestViewSetBase
from faker import Faker

fake = Faker()
MAX_RETRIES = 5

class TestUserViewSet(TestViewSetBase):
    basename = "users"

    def generate_user_attributes(self, username):
        return {
            "username": username,
            "first_name": "John",
            "last_name": "Smith",
            "email": f"{username}@test.com",
            "date_of_birth": "2000-01-01",
            "phone": "+79000000000",
            "role": "developer",
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        for _ in range(MAX_RETRIES):
            username = fake.user_name()
            user_attributes = self.generate_user_attributes(username)

            try:
                user = self.create(user_attributes)
                expected_response = self.expected_details(user, user_attributes)
                assert user == expected_response
                break
            except AssertionError as e:
                if "user with this username already exists." in str(e):
                    continue
                else:
                    raise e
        else:
            assert False, "Failed to create a unique user after multiple retries"

