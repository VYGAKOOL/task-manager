from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task.forms import SignUpForm
from task.models import Task


class WelcomeView(generic.TemplateView):
    template_name = "task/welcome_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm()
        context["register_form"] = SignUpForm()
        return context

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    success_url = reverse_lazy("task:task-list")

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    success_url = reverse_lazy("task:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"label": "Tasks", "url": reverse("task:task-list")},
            {"label": self.object.name, "url": reverse("task:task-detail", args=[self.object.id])},
            {"label": "Edit"},
        ]
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        context["breadcrumbs"] = [
            {"label": "Tasks", "url": reverse("task:task-list")},
            {"label": task.name},
        ]
        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        context["breadcrumbs"] = [
            {"label": "Tasks", "url": reverse("task:task-list")},
            {"label": task.name, "url": reverse("task:task-detail", args=[task.id])},
            {"label": "Delete"},
        ]
        return context


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("login")


class TaskToggleCompleteView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect("task:task-detail", pk=pk)
