from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Worker, Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
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
