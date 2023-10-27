from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from main.models import Task
from django.urls import reverse

CustomUser = get_user_model()


class PermissionsTests(APITestCase):
    token_url = reverse("token_obtain_pair")

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="not_staff_user", password="123"
        )

        self.staff_user = CustomUser.objects.create_user(
            username="staff_user", password="123", is_staff=True
        )

        self.task = Task.objects.create(name="Test Task", author=self.user)

    def test_delete_task_staff(self):
        self.client.login(username="staff_user", password="123")

        response = self.client.post(
            self.token_url, data={"username": "staff_user", "password": "123"}
        )
        JWT_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {JWT_token}")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_user(self):
        self.client.login(username="not_staff_user", password="123")

        response = self.client.post(
            self.token_url, data={"username": "not_staff_user", "password": "123"}
        )
        JWT_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {JWT_token}")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
