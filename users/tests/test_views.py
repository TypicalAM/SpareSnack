"""Test models for the users app"""

from django.test import Client, TestCase


class TestModels(TestCase):
    """Test the models functionality"""

    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
