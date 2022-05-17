from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email='testtags@dev.com', password='testtagpass'):
    """Helper function for creating Users"""
    return get_user_model().objects.create_user(email, password)


class PublicTagsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        resp = self.client.get(TAGS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        Tag.object.create(user=self.user, name='Rum')
        Tag.object.create(user=self.user, name='Gin')
        Tag.object.create(user=self.user, name='Whisky')

        resp = self.client.get(TAGS_URL)
        tags = Tag.object.all()  # queryset that returns all Tags in db
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)  # confirm that response and db queryset match

    def test_tags_only_for_authed_user(self):
        """Testing that users can only see tags submitted by themselves"""

        # this tag should not display for the auth'd user
        Tag.object.create(user=create_user('user2tags@dev.com'), name='Should not be visible to authenticated')

        tag = Tag.object.create(user=self.user, name='Should be visible to authenticated')

        resp = self.client.get(TAGS_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # there should only be one tag returned because only 1 tag was submitted by the auth'd user (self.user)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], tag.name)