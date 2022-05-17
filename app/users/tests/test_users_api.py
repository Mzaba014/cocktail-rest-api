from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_ENDPOINT = reverse('users:create')
UPDATE_SELF_ENDPOINT = reverse('users:self')


def create_user(email, password):
    """Helper function for creating Users"""
    return get_user_model().objects.create_user(email, password)


class PublicUsersAPITests(TestCase):
    """Test API requests that do not require authentication"""

    def setUp(self):
        """Creation of API client for use in other test cases"""
        self.client = APIClient()

    def test_create_valid_user(self):
        """Check that User is created successfully and that we are leveraging our custom User model which encrypts
        the pass"""
        payload = {
            'email': "test@manny.dev",
            'password': "password",
        }

        resp = self.client.post(CREATE_USER_ENDPOINT, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**resp.data)  # retrieves the new user based on the HTTP response data
        self.assertTrue(
            user.check_password(payload['password']))  # check that the password is encrypted in the response
        self.assertNotIn('password', resp.data)

    def test_unauthorized_user_retrieval(self):
        """Test that unauthorized users cannot retrieve User records"""
        resp = self.client.get(UPDATE_SELF_ENDPOINT)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersAPITests(TestCase):
    def setUp(self):
        """Create sample user and authenticate as that user"""
        self.client = APIClient()
        self.user = create_user(
            email='privatetest@manny.dev',
            password='privateuserpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_logged_in_user(self):
        """Test the retrieval of the User object for the authenticated user"""
        resp = self.client.get(UPDATE_SELF_ENDPOINT)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {
            'email': self.user.email
        })

    def test_posts_not_allowed_myself(self):
        """Make sure that POSTs are not allowed against the update myself endpoint"""
        res = self.client.post(UPDATE_SELF_ENDPOINT, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_myself(self):
        """Perform an update against the test user and confirm the changes are made"""
        payload = {'email': 'newprivatetest@manny.dev',
                   'password': 'newprivatepassword'}

        resp = self.client.patch(UPDATE_SELF_ENDPOINT, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
