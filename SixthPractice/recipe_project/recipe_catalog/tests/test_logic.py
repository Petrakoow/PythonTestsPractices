from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Ingredient, Recipe, RecipeIngredients


class TestRecipeCreation(TestCase):
    """Тесты для создания рецептов"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_create_recipe(self):
        """Проверка создания рецепта"""
        url = reverse('add_recipe')
        data = {'name': 'Торт'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.first().author, self.user)

    def tearDown(self):
        """Удаление тестового пользователя"""
        self.user.delete()


class TestIngredientCreation(TestCase):
    """Тесты для создания ингредиентов"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_create_ingredient(self):
        """Проверка создания ингредиента"""
        url = reverse('add_ingredient')
        data = {'name': 'Сахар', 'measuring': 'грамм', 'cost': 0.1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ingredient.objects.count(), 1)

    def tearDown(self):
        """Удаление тестового пользователя"""
        self.user.delete()


class TestRecipeAccess(TestCase):
    """Тесты на проверку прав доступа"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        self.recipe = Recipe.objects.create(name="Пирог", author=self.user)

    def test_recipe_access_for_author(self):
        """Проверка, что только автор может редактировать рецепт"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('edit_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_access_for_non_author(self):
        """Проверка, что не автор не может редактировать рецепт"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('edit_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_deletion_for_author(self):
        """Проверка, что только автор может удалить рецепт"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('delete_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_deletion_for_non_author(self):
        """Проверка, что не автор не может удалить рецепт"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('delete_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """Удаление пользователей и рецепта"""
        self.user.delete()
        self.other_user.delete()
        self.recipe.delete()


class TestIngredientAccess(TestCase):
    """Тесты на проверку прав доступа к ингредиентам"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        self.recipe = Recipe.objects.create(name="Пирог", author=self.user)
        self.ingredient = Ingredient.objects.create(name="Сахар", measuring="грамм", cost=0.1)
        self.recipe_ingredient = RecipeIngredients.objects.create(recipe=self.recipe,
                                                                  ingredient=self.ingredient,
                                                                  measure=5, measure_weight=10)

    def test_edit_ingredient_for_author(self):
        """Проверка, что только автор рецепта может редактировать ингредиент"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('edit_ingredient_form', kwargs={'recipe_id': self.recipe.id, 'ingredient_id': self.ingredient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_ingredient_for_non_author(self):
        """Проверка, что не автор не может редактировать ингредиент"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('edit_ingredient_form', kwargs={'recipe_id': self.recipe.id, 'ingredient_id': self.ingredient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_ingredient_for_author(self):
        """Проверка, что только автор может удалить ингредиент"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('delete_ingredient', kwargs={'recipe_id': self.recipe.id})
        response = self.client.post(url, {'ingredient_ids': [self.ingredient.id]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RecipeIngredients.objects.count(), 0)

    def test_delete_ingredient_for_non_author(self):
        """Проверка, что не автор не может удалить ингредиент"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('delete_ingredient', kwargs={'recipe_id': self.recipe.id})
        response = self.client.post(url, {'ingredient_ids': [self.ingredient.id]})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """Удаление пользователей, ингредиентов и рецепта"""
        self.user.delete()
        self.other_user.delete()
        self.ingredient.delete()
        self.recipe.delete()
        self.recipe_ingredient.delete()
