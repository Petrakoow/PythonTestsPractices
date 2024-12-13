from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class URLAccessTests(TestCase):

    def setUp(self):
        """Настройка тестового пользователя и URL-ов."""
        self.login_url = reverse('login')
        self.registration_url = reverse('registration')
        self.about_url = reverse('about-us')
        self.main_url = reverse('main')
        self.recipe_details_url = reverse('recipe-information', args=[1])
        self.add_recipe_url = reverse('add-recipe')
        self.user_credentials = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_access_main_page_unauthenticated(self):
        """Проверка, что неавторизованные пользователи могут получить доступ к главной странице."""
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)

    def test_access_about_us_unauthenticated(self):
        """Проверка, что неавторизованные пользователи могут получить доступ к странице 'О нас'."""
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)

    def test_access_registration_page_unauthenticated(self):
        """Проверка, что неавторизованные пользователи могут получить доступ к странице регистрации."""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)

    def test_access_login_page_unauthenticated(self):
        """Проверка, что неавторизованные пользователи могут получить доступ к странице входа."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_access_add_recipe_authenticated(self):
        """Проверка, что авторизованные пользователи могут получить доступ к странице добавления рецепта."""
        self.client.login(**self.user_credentials)
        response = self.client.get(self.add_recipe_url)
        self.assertEqual(response.status_code, 200)

    def test_access_add_recipe_unauthenticated(self):
        """Проверка, что неавторизованные пользователи не могут получить доступ к странице добавления рецепта."""
        response = self.client.get(self.add_recipe_url)
        self.assertEqual(response.status_code, 302)

    def test_access_main_page_authenticated(self):
        """Проверка, что авторизованные пользователи могут получить доступ к главной странице."""
        self.client.login(**self.user_credentials)
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)

    def test_access_about_us_authenticated(self):
        """Проверка, что авторизованные пользователи могут получить доступ к странице 'О нас'."""
        self.client.login(**self.user_credentials)
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)

    def test_access_manage_recipes_authenticated(self):
        """Проверка, что авторизованные пользователи могут получить доступ к странице управления рецептами."""
        self.client.login(**self.user_credentials)
        manage_recipes_url = reverse('manage-recipes')
        response = self.client.get(manage_recipes_url)
        self.assertEqual(response.status_code, 200)

    def test_access_manage_recipes_unauthenticated(self):
        """Проверка, что неавторизованные пользователи не могут получить доступ к странице управления рецептами."""
        manage_recipes_url = reverse('manage-recipes')
        response = self.client.get(manage_recipes_url)
        self.assertEqual(response.status_code, 302) 

    def test_access_manage_ingredients_authenticated(self):
        """Проверка, что авторизованные пользователи могут получить доступ к странице управления ингредиентами."""
        self.client.login(**self.user_credentials)
        manage_ingredients_url = reverse('manage-ingredients')
        response = self.client.get(manage_ingredients_url)
        self.assertEqual(response.status_code, 200)

    def test_access_manage_ingredients_unauthenticated(self):
        """Проверка, что неавторизованные пользователи не могут получить доступ к странице управления ингредиентами."""
        manage_ingredients_url = reverse('manage-ingredients')
        response = self.client.get(manage_ingredients_url)
        self.assertEqual(response.status_code, 302)  

    def test_access_recipe_details_unauthenticated(self):
        """Проверка, что неавторизованные пользователи не могут получить доступ к странице деталей рецепта."""
        response = self.client.get(self.recipe_details_url)
        self.assertEqual(response.status_code, 404) 
