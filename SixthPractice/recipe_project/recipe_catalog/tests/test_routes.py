from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from recipe_catalog.models import Ingredient, Recipe


User = get_user_model()


class TestRoutes(TestCase):
    ADMIN_URL = '/admin/'

    @classmethod
    def setUpTestData(cls):
        cls.anonim_user = User.objects.create(username='anonim')
        cls.admin = User.objects.create(username='admin', is_staff=True)

        cls.ingredient_flour = Ingredient.objects.create(
            title='Мука',
            raw_weight=50,
            cooked_weight=50,
            cost=15
        )
        cls.recipe = Recipe.objects.create(title='Парфе')
        cls.recipe.ingredients.set([cls.ingredient_flour])

    def setUp(self):
        self.client_anonim = Client()
        self.client_admin = Client()
        self.client_admin.force_login(self.admin)

    def test_home_page(self):
        urls = [
            (self.client_anonim, reverse('index')),
            (self.client_admin, reverse('index'))
        ]
        for client, url in urls:
            response = client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'recipe_catalog/index.html')

    def test_about_page(self):
        urls = [
            (self.client_anonim, reverse('about')),
            (self.client_admin, reverse('about'))
        ]
        for client, url in urls:
            response = client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'recipe_catalog/about.html')

    def test_recipe_detail_page(self):
        url = reverse('recipe_detail', args=[self.recipe.pk])
        for client in [self.client_anonim, self.client_admin]:
            response = client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, 'recipe_catalog/recipe.html')

    def test_admin_panel_access(self):
        urls = [
            (self.client_admin, self.ADMIN_URL, HTTPStatus.OK),
            (self.client_anonim, self.ADMIN_URL, HTTPStatus.FOUND)
        ]
        for client, url, expected_status in urls:
            response = client.get(url)
            self.assertEqual(response.status_code, expected_status)

