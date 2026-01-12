from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from task.models import Task, TaskType, Position

User = get_user_model()


class BaseTaskTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now().date(),
            priority="medium",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)


class WelcomeViewTest(TestCase):
    def test_welcome_page_loads(self):
        response = self.client.get(reverse("task:welcome"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("login_form", response.context)
        self.assertIn("register_form", response.context)


class TaskListViewTest(BaseTaskTestCase):
    def test_login_required(self):
        response = self.client.get(reverse("task:task-list"))
        self.assertEqual(response.status_code, 302)

    def test_task_list_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("task:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)


class TaskCreateViewTest(BaseTaskTestCase):
    def test_create_task(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("task:task-create"),
            {
                "name": "New task",
                "description": "Desc",
                "deadline": timezone.now().strftime("%Y-%m-%d"),
                "priority": "high",
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        self.assertTrue(Task.objects.filter(name="New task").exists())
        self.assertIn(response.status_code, [200, 302])


class TaskDetailViewTest(BaseTaskTestCase):
    def test_task_detail(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("task:task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)


class TaskUpdateViewTest(BaseTaskTestCase):
    def test_update_task(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("task:task-update", args=[self.task.id]),
            {
                "name": "Updated name",
                "description": self.task.description,
                "deadline": self.task.deadline.strftime("%Y-%m-%d"),
                "priority": self.task.priority,
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated name")
        self.assertIn(response.status_code, [200, 302])


class TaskDeleteViewTest(BaseTaskTestCase):
    def test_delete_task(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("task:task-delete", args=[self.task.id]))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        self.assertIn(response.status_code, [200, 302])


class TaskToggleCompleteViewTest(BaseTaskTestCase):
    def test_toggle_complete(self):
        self.client.login(username="testuser", password="testpass123")
        self.assertFalse(self.task.is_completed)
        response = self.client.post(reverse("task:task-toggle", args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertIn(response.status_code, [200, 302])
