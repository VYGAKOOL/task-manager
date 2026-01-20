from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Position

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "position")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "position", "is_active")
