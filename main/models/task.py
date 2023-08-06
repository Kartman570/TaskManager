from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class State(models.TextChoices):
        NEW = "New"
        DEVELOPMENT = "Development"
        QA = "Qa"
        CODE_REVIEW = "Code review"
        READY_FOR_RELEASE = "Ready for release"
        RELEASED = "Released"
        Archived = "Archived"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField()
    state = models.CharField(max_length=255, choices=State.choices, default=State.NEW)
    priority = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="worker")
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tag")

    def __str__(self):
        return self.name
