from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='test@manny.dev', password='modelstestpass'):
    """Helper function for creating Users"""
    return get_user_model().objects.create_user(email, password)


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

    def test_create_superuser(self):
        """Test creation of a User with is_superuser and is_admin, aka a SuperUser"""
        email = 'test@manny.dev'
        password = 'test_pass'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_email_normalization(self):
        """Test that the domain segment of the email is normalized when new user is created"""
        email = 'test@MANNY.DEV'
        user = get_user_model().objects.create_user(email, 'test_pass')

        self.assertEqual(user.email, email.lower())

    def test_email_validation(self):
        """Test that creating a user with no email raises an exception"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test_pass')

    def test_password_validation(self):
        """Test that creating a user with no password raises an exception"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@manny.dev', None)

    def test_create_tag(self):
        tag = models.Tag.objects.create(
            submitted_by=create_user(),
            name='Gin'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        ingredient = models.Ingredient.objects.create(
            submitted_by=create_user(),
            name='Demerara syrup',
            quantity='1oz'
        )

        self.assertEqual(str(ingredient), ingredient.name)