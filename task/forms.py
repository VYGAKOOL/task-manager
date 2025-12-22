from django.contrib.auth.forms import UserCreationForm

from task.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "password1", "password2", "position")
