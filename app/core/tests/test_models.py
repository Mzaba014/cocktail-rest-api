from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user(self):
        """Test creation of a user with an email as the username, a custom functionality defined in our User model"""

        email = 'test@manny.dev'
        password = 'test_pass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(
            user.check_password(password))  # must use provided check_pass helper bc passwords are auto-hashed
