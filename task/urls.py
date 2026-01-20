from django.urls import path

from task.views import (
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    WelcomeView,
    TaskToggleCompleteView,
)

app_name = "task"
urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "<int:pk>/toggle/",
        TaskToggleCompleteView.as_view(),
        name="task-toggle"
    ),
]
