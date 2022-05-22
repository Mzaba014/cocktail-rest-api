from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipes.serializers import TagSerializer

TAGS_URL = reverse('recipes:tag-list')


def create_user(email='testtags@dev.com', password='testtagpass'):
    """Helper function for creating Users"""
    return get_user_model().objects.create_user(email, password)


class PublicTagsAPITests(TestCase):
    def setUp(self):
        """Creates shared APIClient instance"""
        self.client = APIClient()

    def test_login_required(self):
        resp = self.client.get(TAGS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    def setUp(self):
        """Create a user and authenticate as that user"""

        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        """Testing creation and retrieval of Tags"""

        Tag.objects.create(submitted_by=self.user, name='Rum')
        Tag.objects.create(submitted_by=self.user, name='Gin')
        Tag.objects.create(submitted_by=self.user, name='Whisky')

        resp = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')  # queryset that returns all Tags in db ordered by name desc
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)  # confirm that Tag API response and db queryset match

    def test_tags_only_for_authed_user(self):
        """Testing that users can only see tags submitted by themselves"""

        Tag.objects.create(submitted_by=create_user('user2tags@dev.com'), name='Should not be visible to authenticated')
        tag = Tag.objects.create(submitted_by=self.user, name='Should be visible to authenticated')

        resp = self.client.get(TAGS_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # there should only be one tag returned because only 1 tag was submitted by the auth'd user (self.user)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], tag.name)

    def test_create_tag(self):
        payload = {'name': 'Test tag creation'}
        self.client.post(TAGS_URL, payload)

        created_success = Tag.objects.filter(
            submitted_by=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(created_success)

    def test_invalid_tag(self):
        payload = {'name': ''}
        resp = self.client.post(TAGS_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)