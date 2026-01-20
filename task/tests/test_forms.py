from django.test import TestCase
from datetime import date

from accounts.models import Position, Worker
from task.forms import TaskForm
from task.models import TaskType
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user1 = Worker.objects.create_user(
            username="user1", password="pass12345", position=self.position
        )
        self.user2 = Worker.objects.create_user(
            username="user2", password="pass12345", position=self.position
        )
        self.task_type_bug = TaskType.objects.create(name="Bug")
        self.task_type_feature = TaskType.objects.create(name="Feature")

    def test_task_form_valid_data(self):
        form = TaskForm(
            data={
                "name": "Fix login bug",
                "description": "Users cannot login",
                "deadline": date(2030, 1, 1),
                "priority": "high",
                "task_type": self.task_type_bug.id,
                "assignees": [self.user1.id, self.user2.id],
            }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_task_form_optional_assignees(self):
        form = TaskForm(
            data={
                "name": "Add new feature",
                "description": "Implement payment gateway",
                "deadline": date(2030, 1, 1),
                "priority": "low",
                "task_type": self.task_type_feature.id,
            }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())
