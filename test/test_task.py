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
        task = self.create(task_attributes)
        expected_response = self.expected_details(task, task_attributes)
        
        now = datetime.now()#check for AUTO date-time fields in models
        created_date = datetime.fromisoformat(task["created_date"].replace("Z", ""))
        changed_date = datetime.fromisoformat(task["changed_date"].replace("Z", ""))
        assert now - timedelta(seconds=1) <= created_date <= now + timedelta(seconds=1)
        assert now - timedelta(seconds=1) <= changed_date <= now + timedelta(seconds=1)
        
        del task["created_date"]#if date is OK, check else
        del task["changed_date"]
        assert task == expected_response


    def test_update(self):
        task_attributes = self.generate_task_attributes()
        task = self.create(task_attributes)
        new_data = self.generate_task_attributes()
        updated_attributes = {**task, **new_data}

        expected_response = self.expected_details(task, updated_attributes)
        response = self.update(new_data, task["id"])
        assert response == expected_response

    def test_delete(self):
        task_attributes = self.generate_task_attributes()
        task = self.create(task_attributes)
        
        response = self.delete(task["id"])
        expected_response = HTTPStatus.NO_CONTENT
        assert response == expected_response

    def test_list(self):
        tasks_list = []
        for i in range(5):
            task_attributes = self.generate_task_attributes()
            task = self.create(task_attributes)
            tasks_list.append(task)
        
        expected_response = tasks_list
        response = self.list()
        assert response == expected_response

    def test_retrieve(self):
        tasks_list = []
        for i in range(5):
            task_attributes = self.generate_task_attributes()
            task = self.create(task_attributes)
            tasks_list.append(task)
        
        expected_response = tasks_list[2]
        response = self.retrieve(tasks_list[2]['id'])
        assert response == expected_response
