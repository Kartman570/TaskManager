from test.base import TestViewSetBase
from faker import Faker
from http import HTTPStatus

fake = Faker()


class TestTagViewSet(TestViewSetBase):
    basename = "tags"

    def generate_tag_attributes(self):
        return {
            "name": fake.user_name(),
        }

    def generate_test_data(self, data_count: int):
        expected_response = []
        for _ in range(data_count):
            tag_attributes = self.generate_tag_attributes()
            tag = self.create(tag_attributes)
            expected_response.append(tag.data)
        return expected_response

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag_attributes = self.generate_tag_attributes()
        response = self.create(tag_attributes)
        expected_response = self.expected_details(response.data, tag_attributes)
        assert response.status_code == HTTPStatus.CREATED
        assert response.data == expected_response

    def test_update(self):
        tag_attributes = self.generate_tag_attributes()
        tag = self.create(tag_attributes)
        new_data = self.generate_tag_attributes()
        updated_attributes = {**tag.data, **new_data}

        expected_response = self.expected_details(tag.data, updated_attributes)
        response = self.update(new_data, tag.data["id"])
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response

    def test_delete(self):
        tag_attributes = self.generate_tag_attributes()
        tag = self.create(tag_attributes)

        response = self.delete(tag.data["id"])
        assert response.status_code == HTTPStatus.NO_CONTENT
        new_response = self.retrieve(tag.data["id"])
        assert new_response.status_code == HTTPStatus.NOT_FOUND

    def test_list(self):
        expected_response = self.generate_test_data(5)
        response = self.list()
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response

    def test_retrieve(self):
        expected_response = self.generate_test_data(1)
        response = self.retrieve(expected_response[0]["id"])
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response[0]