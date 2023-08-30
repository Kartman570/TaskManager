from test.base import TestViewSetBase
from faker import Faker
from datetime import datetime, timedelta
from http import HTTPStatus

fake = Faker()


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    def generate_task_attributes(self):
        self.tag = self.create_test_tag()
        return {
            "name": fake.user_name(),
            "description": fake.pystr(),
            "deadline_date": fake.future_datetime().isoformat() + "Z",
            "author": self.user.id,
            "worker": self.user.id,
            "tags": self.tag.id,
            "state": "New",
            "priority": 1,
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        task_attributes = self.generate_task_attributes()
        response = self.create(task_attributes)
        expected_response = self.expected_details(response.data, task_attributes)

        assert self.is_auto_date_time_correct(response.data["created_date"])
        assert self.is_auto_date_time_correct(response.data["changed_date"])

        del response.data["created_date"]  # if date is OK, check else
        del response.data["changed_date"]
        assert response.data == expected_response

    def is_auto_date_time_correct(self, time: str):
        now = datetime.now()
        date_to_check = datetime.fromisoformat(time.replace("Z", ""))
        return now - timedelta(seconds=1) <= date_to_check <= now + timedelta(seconds=1)

    def test_update(self):
        task_attributes = self.generate_task_attributes()
        task = self.create(task_attributes)
        new_data = self.generate_task_attributes()
        updated_attributes = {**task.data, **new_data}

        expected_response = self.expected_details(task.data, updated_attributes)
        response = self.update(new_data, task.data["id"])
        assert response.data == expected_response

    def test_delete(self):
        task_attributes = self.generate_task_attributes()
        task = self.create(task_attributes)

        response = self.delete(task.data["id"])
        assert response.status_code == HTTPStatus.NO_CONTENT
        new_response = self.retrieve(task.data["id"])
        assert new_response.status_code == HTTPStatus.NOT_FOUND

    def test_list(self):
        tasks_list = []
        for i in range(5):
            task_attributes = self.generate_task_attributes()
            task = self.create(task_attributes)
            tasks_list.append(task.data)

        expected_response = tasks_list
        response = self.list()
        assert response.data == expected_response

    def test_retrieve(self):
        tasks_list = []
        for i in range(5):
            task_attributes = self.generate_task_attributes()
            task = self.create(task_attributes)
            tasks_list.append(task.data)

        expected_response = tasks_list[2]
        response = self.retrieve(tasks_list[2]["id"])
        assert response.data == expected_response