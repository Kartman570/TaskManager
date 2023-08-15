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
    deadline_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=255, choices=State.choices, default=State.NEW)
    priority = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    worker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="worker", null=True, blank=True
    )
    tags = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tag", null=True, blank=True
    )

    def __str__(self):
        return self.name
