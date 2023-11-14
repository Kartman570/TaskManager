from main.models import Task, Tag
from test.base import TestViewSetBase
from main.serializers import TaskSerializer, TagSerializer
from typing import List


class TestTasksTagsViewSet(TestViewSetBase):
    basename = "task_tags"

    def test_list(self) -> None:
        task = self.create_test_task()
        tag1 = self.create_test_tag()
        tag2 = self.create_test_tag()
        self.add_tags(task, [tag1, tag2])

        tags = self.list(args=[task.id]).data

        tag1 = TagSerializer(tag1).data
        tag2 = TagSerializer(tag2).data
        assert tags == [tag1, tag2]

    def ids(self, tags: List[Tag]):
        return [tag.id for tag in tags]

    def add_tags(self, task: dict, tags: list) -> None:
        task = TaskSerializer(task).data
        task_instance = Task.objects.get(pk=task["id"])
        task_instance.tags.add(*self.ids(tags))
        task_instance.save()
