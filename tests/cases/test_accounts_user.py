"""
Example: Accounts — User creation tests.

Run:
    python manage.py test tests.cases.test_accounts_user
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationTestCase(TestCase):
    """Test cases for user creation via UserManager."""

    def setUp(self):
        self.email = "test@example.com"
        self.password = "StrongPass123!"

    def test_create_regular_user(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="admin@example.com", password=self.password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=self.password)

    def test_get_full_name(self):
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.get_full_name(), "John Doe")

    def test_get_full_name_fallback_to_email(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(user.get_full_name(), self.email)
