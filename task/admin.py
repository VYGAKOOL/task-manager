from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Position, TaskType, Worker, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "position",
        "is_staff",
        "is_active",
    )
    list_filter = ("position", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("position",)}),)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type", "priority", "is_completed", "deadline")
    list_filter = ("priority", "task_type", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
    ordering = ("-deadline",)
