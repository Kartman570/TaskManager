from test.base import TestViewSetBase
from faker import Faker
from http import HTTPStatus

fake = Faker()

class TestUserViewSet(TestViewSetBase):
    basename = "tags"
    def generate_tag_attributes(self):
        return {
            "name": fake.user_name(),
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag_attributes = self.generate_tag_attributes()
        tag = self.create(tag_attributes)
        expected_response = self.expected_details(tag, tag_attributes)
        assert tag == expected_response


    def test_update(self):
        tag_attributes = self.generate_tag_attributes()
        tag = self.create(tag_attributes)
        new_data = self.generate_tag_attributes()
        updated_attributes = {**tag, **new_data}

        expected_response = self.expected_details(tag, updated_attributes)
        response = self.update(new_data, tag["id"])
        assert response == expected_response

    def test_delete(self):
        tag_attributes = self.generate_tag_attributes()
        tag = self.create(tag_attributes)
        
        response = self.delete(tag["id"])
        expected_response = HTTPStatus.NO_CONTENT
        assert response == expected_response

    def test_list(self):
        tags_list = []
        for i in range(5):
            tag_attributes = self.generate_tag_attributes()
            tag = self.create(tag_attributes)
            tags_list.append(tag)
        
        expected_response = tags_list
        response = self.list()
        assert response == expected_response

    def test_retrieve(self):
        tags_list = []
        for i in range(5):
            tag_attributes = self.generate_tag_attributes()
            tag = self.create(tag_attributes)
            tags_list.append(tag)
        
        expected_response = tags_list[2]
        response = self.retrieve(tags_list[2]['id'])
        assert response == expected_response
