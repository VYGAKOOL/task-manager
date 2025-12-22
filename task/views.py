from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from task.forms import WorkerCreationForm
from task.models import Task


class WelcomeView(generic.TemplateView):
    template_name = "task/welcome_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm()
        context["register_form"] = WorkerCreationForm()
        return context

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("task:task-list")

class TaskUpdateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]


class TaskDetailView(LoginRequiredMixin, generic.CreateView):
    model = Task
    context_object_name = "task"


class TaskDeleteView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class RegisterView(generic.View):
    def post(self, request):
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return redirect("task:welcome")