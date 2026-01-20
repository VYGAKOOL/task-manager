from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Position, Worker

User = get_user_model()


class SignUpViewTests(TestCase):
    def setUp(self):
        self.url = reverse("accounts:sign-up")
        self.user_data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
        }

    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/sign_up.html")

    def test_signup_view_post_creates_user_and_logs_in(self):
        response = self.client.post(self.url, self.user_data)
        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)
        user = User.objects.get(username="newuser")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        self.assertRedirects(response, reverse("task:task-list"))


class WorkerListViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.user = Worker.objects.create_user(
            username="worker1",
            email="worker1@test.com",
            password="Password123",
            position=self.position
        )
        self.url = reverse("accounts:account-list")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_view_with_permission(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workers/worker_list.html")
        self.assertIn("workers", response.context)


class WorkerUpdateViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.user = Worker.objects.create_user(
            username="worker1",
            email="worker1@test.com",
            password="Password123",
            position=self.position
        )
        self.url = reverse("accounts:account-edit", args=[self.user.pk])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_update_worker_email(self):
        self.client.force_login(self.user)
        new_email = "updated@test.com"
        response = self.client.post(self.url, {
            "email": new_email,
            "username": self.user.username,
            "position": self.position.pk
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)
        self.assertRedirects(response, reverse("accounts:account-list"))
