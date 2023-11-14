from test.base import TestViewSetBase
from faker import Faker
from datetime import datetime, timedelta
from http import HTTPStatus
from freezegun import freeze_time
from test.factory_base import TaskFactory, TagFactory
import factory

fake = Faker()
frozen_time = str(datetime.now().isoformat() + "Z")


@freeze_time(frozen_time)
class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def create_task_attributes(self):
        task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)
        task_attributes["author"] = self.user.id
        task_attributes["worker"] = self.user.id
        test_tag = self.create_test_tag()
        task_attributes["tags"] = [test_tag.id]
        return task_attributes

    def test_create(self):
        global frozen_time
        task_attributes = self.create_task_attributes()

        response = self.create(task_attributes)
        date_time = {"created_date": frozen_time, "changed_date": frozen_time}

        task_attributes.update(date_time)

        expected_response = self.expected_details(response.data, task_attributes)
        assert response.status_code == HTTPStatus.CREATED
        assert response.data == expected_response

    def test_update(self):
        task_attributes = self.create_task_attributes()
        task = self.create(task_attributes)
        new_data = self.create_task_attributes()
        updated_attributes = {**task.data, **new_data}

        expected_response = self.expected_details(task.data, updated_attributes)
        response = self.update(new_data, task.data["id"])
        assert response.status_code == HTTPStatus.OK
        assert response.data == expected_response

    def test_delete(self):
        task_attributes = self.create_task_attributes()
        task = self.create(task_attributes)
        response = self.delete(task.data["id"])
        assert response.status_code == HTTPStatus.NO_CONTENT
        new_response = self.retrieve(task.data["id"])
        assert new_response.status_code == HTTPStatus.NOT_FOUND

    def create_many_tasks(self, count: int) -> list:
        tasks_list = []
        for _ in range(count):
            task_attributes = self.create_task_attributes()
            task = self.create(task_attributes)
            tasks_list.append(task.data)
        return tasks_list

    def test_list(self):
        tasks_list = self.create_many_tasks(5)

        expected_response = tasks_list
        response = self.list()
        assert response.data == expected_response

    def test_retrieve(self):
        tasks_list = self.create_many_tasks(5)

        expected_response = tasks_list[2]
        response = self.retrieve(tasks_list[2]["id"])
        assert response.data == expected_response
