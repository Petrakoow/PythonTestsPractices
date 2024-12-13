from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipe_catalog.models import Ingredient, Unit
from recipe_catalog.forms import IngredientForm
from django.test import Client

class IngredientTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.unit = Unit.objects.create(name='g', conversion_to_grams=1.0, author=self.user)

    def test_add_ingredient(self):
        url = reverse('add-ingredient')
        data = {
            'title': 'Test Ingredient',
            'raw_weight': 100.0,
            'cooked_weight': 80.0,
            'cost': 5.0,
            'unit': self.unit.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Ingredient.objects.count(), 1) 
        ingredient = Ingredient.objects.first()
        self.assertEqual(ingredient.title, 'Test Ingredient')

    def test_edit_ingredient(self):
        ingredient = Ingredient.objects.create(
            title='Old Ingredient',
            raw_weight=100.0,
            cooked_weight=80.0,
            cost=5.0,
            unit=self.unit,
            author=self.user
        )
        url = reverse('edit-ingredient-element', kwargs={'pk': ingredient.id})
        data = {
            'title': 'Updated Ingredient',
            'raw_weight': 120.0,
            'cooked_weight': 90.0,
            'cost': 6.0,
            'unit': self.unit.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) 
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.title, 'Updated Ingredient')
        self.assertEqual(ingredient.raw_weight, 120.0)
        self.assertEqual(ingredient.cooked_weight, 90.0)
        self.assertEqual(ingredient.cost, 6.0)

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(
            title='Delete Me',
            raw_weight=100.0,
            cooked_weight=80.0,
            cost=5.0,
            unit=self.unit,
            author=self.user
        )
        url = reverse('delete-ingredient-element', kwargs={'pk': ingredient.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Ingredient.objects.count(), 0)  

    def test_manage_ingredients(self):
        Ingredient.objects.create(
            title='Ingredient 1',
            raw_weight=100.0,
            cooked_weight=80.0,
            cost=5.0,
            unit=self.unit,
            author=self.user
        )
        url = reverse('manage-ingredients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ingredient 1')

    def test_invalid_add_ingredient(self):
        url = reverse('add-ingredient')
        data = {
            'title': '',  
            'raw_weight': -100.0, 
            'cooked_weight': 80.0,
            'cost': 5.0,
            'unit': self.unit.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertFormError(response, 'form', 'title', 'Обязательное поле.')
        self.assertFormError(response, 'form', 'raw_weight', 'Сырой вес должен быть положительным числом.')

