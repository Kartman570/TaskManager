from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from main.services.mail import send_assign_notification
from test.base import TestViewSetBase
from test.factory_base import JWTFactory, TaskFactory


class TestSendEmail(TestViewSetBase):
    @staticmethod
    def create_user():
        return JWTFactory.create()

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.create_user()
        task = TaskFactory.create(worker=assignee, author=assignee)

        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
