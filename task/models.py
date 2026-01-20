from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    class Priority(models.TextChoices):
        URGENT = "urgent", _("Urgent")
        HIGH = "high", _("High")
        MEDIUM = "medium", _("Medium")
        LOW = "low", _("Low")

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )

    task_type = models.ForeignKey(
        TaskType, on_delete=models.PROTECT, related_name="tasks"
    )

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assignees_tasks", blank=True
    )

    def __str__(self):
        return self.name
