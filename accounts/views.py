from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import SignUpForm, WorkerUpdateForm

User = get_user_model()


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("task:task-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class WorkerListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = User
    template_name = "workers/worker_list.html"
    context_object_name = "workers"
    permission_required = "task.view_worker"


class WorkerUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = User
    form_class = WorkerUpdateForm
    template_name = "workers/worker_form.html"
    success_url = reverse_lazy("workers:worker-list")
    permission_required = "task.change_worker"
