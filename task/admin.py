from django.contrib import admin
from task.models import TaskType, Task


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "is_completed",
        "deadline"
    )
    list_filter = ("priority", "task_type", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
    ordering = ("-deadline",)
