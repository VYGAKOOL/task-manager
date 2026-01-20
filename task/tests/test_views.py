from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from accounts.models import Worker, Position
from task.models import Task, TaskType


class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create_user(
            username="testuser",
            password="password123",
            position=self.position
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=date.today() + timedelta(days=5),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_task_list_view(self):
        url = reverse("task:task-list")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_requires_login(self):
        self.client.logout()
        url = reverse("task:task-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_task_detail_view(self):
        url = reverse("task:task-detail", args=[self.task.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view(self):
        url = reverse("task:task-create")
        data = {
            "name": "New Task",
            "description": "Description",
            "deadline": date.today() + timedelta(days=3),
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        url = reverse("task:task-update", args=[self.task.id])
        data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "deadline": date.today() + timedelta(days=10),
            "priority": Task.Priority.LOW,
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        url = reverse("task:task-delete", args=[self.task.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_toggle_complete_view(self):
        url = reverse("task:task-toggle", args=[self.task.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        response = self.client.post(url, follow=True)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
