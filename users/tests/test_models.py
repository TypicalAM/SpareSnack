"""Test models for the users app"""

from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Profile


class TestModels(TestCase):
    """Test the models functionality"""

    def setUp(self) -> None:
        """Create a test user"""
        self.username = "bob"
        self.user = User.objects.create_user(self.username)

        return super().setUp()

    def test_profile_automatic_creation(self) -> None:
        """If we create a user, a signal was sent to create a profile"""
        self.assertTrue(Profile.objects.all())

    def test_profile_ownership_and_default_fields(self) -> None:
        """The Profile should be accessible via the user instance"""
        profile = self.user.profile

        self.assertTrue(profile)
        self.assertEqual(str(profile), f"{self.username}'s Profile")

        self.assertTrue(profile.is_metric)
        self.assertEqual(profile.fats, 0.0)
        self.assertEqual(profile.carbs, 0.0)
        self.assertEqual(profile.protein, 0.0)
