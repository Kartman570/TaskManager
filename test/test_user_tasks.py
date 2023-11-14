from http import HTTPStatus

from test.base import TestViewSetBase
import factory
from test.factory_base import UserFactory, TaskFactory
from main.serializers import UserSerializer, TaskSerializer, TagSerializer


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    def test_list(self) -> None:
        user = self.create_test_user()
        task1 = self.create_test_task(user=user)
        task1 = TaskSerializer(task1).data

        tasks = self.list(args=[user.id]).data

        assert tasks == [task1]

    def test_retrieve_foreign_task(self) -> None:
        user = self.create_test_user()
        user = UserSerializer(user).data
        task = self.create_test_task()
        task = TaskSerializer(task).data

        response = self.retrieve(key=[user["id"], task["id"]])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        user = self.create_test_user()
        created_task = self.create_test_task(user=user)
        user = UserSerializer(user).data
        created_task = TaskSerializer(created_task).data

        retrieved_task = self.retrieve(key=[user["id"], created_task["id"]])

        assert created_task == retrieved_task.data
