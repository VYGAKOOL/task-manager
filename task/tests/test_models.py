from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from task.models import TaskType, Task
from accounts.models import Position

User = get_user_model()


class TaskTypeModelTest(TestCase):
    def test_create_task_type(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(task_type.name, "Bug")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Feature")
        self.assertEqual(str(task_type), "Feature")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")

    def test_create_worker(self):
        user = User.objects.create_user(
            username="john",
            password="password123",
            position=self.position,
        )

        self.assertEqual(user.username, "john")
        self.assertEqual(user.position, self.position)

    def test_worker_str(self):
        user = User.objects.create_user(
            username="alice",
            password="password123",
            position=self.position,
        )
        self.assertEqual(str(user), "alice (Manager)")


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="worker",
            password="password123",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Bug")

    def test_create_task(self):
        task = Task.objects.create(
            name="Fix bug",
            description="Fix critical bug",
            task_type=self.task_type,
            deadline=date.today(),
            priority=Task.Priority.HIGH,
        )

        self.assertEqual(task.name, "Fix bug")
        self.assertEqual(task.priority, Task.Priority.HIGH)
        self.assertFalse(task.is_completed)

    def test_task_default_values(self):
        task = Task.objects.create(
            name="Write tests",
            description="Cover models",
            task_type=self.task_type,
        )

        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)
        self.assertIsNone(task.deadline)

    def test_task_assignees(self):
        task = Task.objects.create(
            name="Assign task",
            description="Assign worker",
            task_type=self.task_type,
        )

        task.assignees.add(self.user)

        self.assertIn(self.user, task.assignees.all())

    def test_task_str(self):
        task = Task.objects.create(
            name="Deploy",
            description="Deploy to prod",
            task_type=self.task_type,
        )

        self.assertEqual(str(task), "Deploy")
