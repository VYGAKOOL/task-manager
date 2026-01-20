from django.urls import path
from accounts.views import SignUpView, WorkerListView, WorkerUpdateView

app_name = "accounts"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("accounts/", WorkerListView.as_view(), name="account-list"),
    path(
        "account/<int:pk>/edit/",
        WorkerUpdateView.as_view(),
        name="account-edit"
    ),
]
