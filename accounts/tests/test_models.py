from django.test import TestCase

from accounts.models import Position


class PositionModelTest(TestCase):
    def test_create_position(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(position.name, "Developer")

    def test_position_str(self):
        position = Position.objects.create(name="QA")
        self.assertEqual(str(position), "QA")
