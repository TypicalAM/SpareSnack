"""Test models for the users app"""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls.base import reverse_lazy


class TestModels(TestCase):
    """Test the models functionality"""

    def setUp(self) -> None:
        """Set up the client and the user to create a profile page"""
        self.client = Client()
        self.user = User.objects.create_user(username="bob")

        return super().setUp()

    def test_profile_get_noaccount(self) -> None:
        """The profile view should redirect to the login page"""
        response = self.client.get(reverse_lazy("account_profile"))

        self.assertRedirects(
            response,
            f'{reverse_lazy("account_login")}?next={reverse_lazy("account_profile")}',
        )

    def test_profile_get(self) -> None:
        """The profile view should return the correct profile instance"""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("account_profile"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("profile/index.html")

        self.assertEqual(response.context.get("user"), self.user)
        self.assertIn("meals", response.context)
        self.assertIn("diets", response.context)

    def test_signup_get(self) -> None:
        """The signup form template check"""
        response = self.client.get(reverse_lazy("account_signup"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_login_get_logged_in(self) -> None:
        """the login page should redirect if you're logged in"""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("account_login"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_login_get(self) -> None:
        """The login form template check"""
        response = self.client.get(reverse_lazy("account_login"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "account/login.html")

    def test_logout_get_not_logged_in(self) -> None:
        """The logout page should redirect to the login page if not logged in"""
        response = self.client.get(reverse_lazy("account_logout"))

        self.assertRedirects(
            response,
            f'{reverse_lazy("account_login")}?next={reverse_lazy("account_logout")}',
        )

    def test_logout_get(self) -> None:
        """The logout page should log you out"""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("account_logout"))

        self.assertRedirects(response, reverse_lazy("foods_meal_browse"))

    def test_password_change_get_not_logged_in(self) -> None:
        """The password change page should redirect if you're not logged in"""
        response = self.client.get(reverse_lazy("account_change_password"))

        self.assertRedirects(
            response,
            f'{reverse_lazy("account_login")}?next={reverse_lazy("account_change_password")}',
        )

    def test_goals_change_get_not_logged_in(self) -> None:
        """The goals change page should redirect when not logged in"""
        response = self.client.get(reverse_lazy("account_change_goals"))

        self.assertRedirects(
            response,
            f'{reverse_lazy("account_login")}?next={reverse_lazy("account_change_goals")}',
        )

    def test_goals_change_get(self) -> None:
        """The goals change page should return the correct profile instance"""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("account_change_goals"))

        self.assertTemplateUsed(response, "profile/change_goals.html")
        self.assertEqual(response.context.get("profile"), self.user.profile)

    def test_avatar_change_get_not_logged_in(self) -> None:
        """The avatar change page should redirect when not logged in"""
        response = self.client.get(reverse_lazy("account_change_avatar"))

        self.assertRedirects(
            response,
            f'{reverse_lazy("account_login")}?next={reverse_lazy("account_change_avatar")}',
        )

    def test_avatar_change_get(self) -> None:
        """The avatar change page should return the correct profile instance"""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("account_change_avatar"))

        self.assertTemplateUsed(response, "profile/change_avatar.html")
        self.assertEqual(response.context.get("profile"), self.user.profile)
