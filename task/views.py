from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from task.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task


class TaskUpdateView(LoginRequiredMixin, generic.CreateView):
    model = Task


class TaskDetailView(LoginRequiredMixin, generic.CreateView):
    model = Task


class TaskDeleteView(LoginRequiredMixin, generic.CreateView):
    model = Task