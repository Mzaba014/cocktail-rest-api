from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipes.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipes:ingredient-list')


def create_user(email='testingredient@dev.com', password='password'):
    """Helper function for creating Users"""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientsApiTests(TestCase):
    """Tests for unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        resp = self.client.get(INGREDIENTS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_ingredient_list(self):
        Ingredient.objects.create(
            name='Demerara syrup',
            submitted_by=self.user,
            quantity='1 oz'
        )

        Ingredient.objects.create(
            name='Lime juice',
            submitted_by=self.user,
            quantity='1 oz'
        )
        resp = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_ingredients_only_for_authed_user(self):
        other_user = create_user('secondingredientuser@dev.com', 'password')
        Ingredient.objects.create(submitted_by=other_user, name='other user ingredient', quantity='1 oz')
        ingredient = Ingredient.objects.create(submitted_by=self.user, name='Lemon juice', quantity='1 oz')

        resp = self.client.get(INGREDIENTS_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], ingredient.name)

    def test_create_ingredient(self):
        payload = {'name': 'Cinnamon syrup', 'quantity': '.5 oz'}
        self.client.post(INGREDIENTS_URL, payload)

        created = Ingredient.objects.filter(
            submitted_by=self.user,
            name=payload['name'],
        ).exists()

        self.assertTrue(created)

    def test_create_invalid_ingredient(self):
        payload = {'name': ''}
        resp = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
