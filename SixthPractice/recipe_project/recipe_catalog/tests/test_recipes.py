from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipe_catalog.models import Recipe
from django.test import Client


class RecipeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_recipe(self):
        url = reverse('add-recipe')
        data = {
            'title': 'Test Recipe',  
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Recipe.objects.count(), 1)  
        recipe = Recipe.objects.first()
        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.author, self.user)

    def test_edit_recipe(self):
        recipe = Recipe.objects.create(title='Old Title', author=self.user)
        url = reverse('edit-recipe', kwargs={'pk': recipe.pk})
        data = {
            'title': 'Updated Title',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Updated Title')

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(title='Test Recipe', author=self.user)
        url = reverse('delete-recipe', kwargs={'pk': recipe.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Recipe.objects.count(), 0) 
