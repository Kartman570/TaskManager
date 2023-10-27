from test.base import TestViewSetBase
from faker import Faker
from http import HTTPStatus
from test.factory_base import TagFactory
import factory
from main.serializers import TagSerializer

fake = Faker()


class TestTagViewSet(TestViewSetBase):
    basename = "tags"

    def generate_test_data(self, data_count: int):
        expected_response = []
        serializer = TagSerializer(self.test_tag)
        expected_response.append(serializer.data)
        for _ in range(data_count):
            tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
            tag = self.create(tag_attributes)
            expected_response.append(tag.data)
        return expected_response

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        response = self.create(tag_attributes)
        expected_response = self.expected_details(response.data, tag_attributes)
        assert response.status_code == HTTPStatus.CREATED
        assert response.data == expected_response

    def test_update(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
        tag = self.create(tag_attributes)
        new_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        updated_attributes = {**tag.data, **new_data}

        expected_response = self.expected_details(tag.data, updated_attributes)
        response = self.update(new_data, tag.data["id"])
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response

    def test_delete(self):
        tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
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
        tag_list = self.generate_test_data(5)
        response = self.retrieve(tag_list[2]["id"])
        expected_response = tag_list[2]
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response
