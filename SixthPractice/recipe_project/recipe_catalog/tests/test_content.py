from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Ingredient, Recipe, RecipeIngredients


class TestMain(TestCase):
    """Тесты для главной страницы"""
    MAIN_PAGE_URL = reverse('main')
    RECIPE_NAME = "Pancakes"

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
        self.recipe = Recipe.objects.create(name=self.RECIPE_NAME, author=self.user)

    def test_status_code(self):
        """Проверка кода состояния главной страницы"""
        response = self.client.get(self.MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        """Проверка наличия 'recipes' в контексте страницы"""
        response = self.client.get(self.MAIN_PAGE_URL)
        self.assertIn('recipes', response.context)

    def test_validate_recipe_name(self):
        """Проверка имени рецепта в контексте страницы"""
        response = self.client.get(self.MAIN_PAGE_URL)
        self.assertEqual(response.context['recipes'][0].name, self.RECIPE_NAME)

    def test_recipes_amount(self):
        """Проверка количества рецептов на главной странице"""
        response = self.client.get(self.MAIN_PAGE_URL)
        self.assertEqual(len(response.context['recipes']), 1)

    def tearDown(self):
        self.user.delete()
        self.recipe.delete()


class TestAbout(TestCase):
    """Тесты для страницы 'О нас'"""
    ABOUT_PAGE_URL = reverse('about')

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    def test_status_code(self):
        """Проверка кода состояния страницы 'О нас'"""
        response = self.client.get(self.ABOUT_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.user.delete()


class TestRecipes(TestCase):
    """Тесты для страницы рецептов"""
    CONTEXT_FIELDS = (
        "recipe",
        "recipe_ingredients",
        "total_cost",
        "total_weight",
    )
    INGREDIENTS = [
        dict(name="Соль", measuring="грамм", cost=0.05, measure=5, measure_weight=5),
        dict(name="Сахар", measuring="грамм", cost=0.1, measure=10, measure_weight=10),
        dict(name="Мука", measuring="грамм", cost=0.2, measure=100, measure_weight=100)
    ]

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

        self.recipe = Recipe.objects.create(name="Блинчики", author=self.user)

        self.ingredients = []
        for ingredient in self.INGREDIENTS:
            self.ingredients.append(Ingredient.objects.create(
                name=ingredient["name"],
                measuring=ingredient["measuring"],
                cost=ingredient["cost"]
            ))

        for ingredient, ingredient_class in zip(self.INGREDIENTS, self.ingredients):
            RecipeIngredients.objects.create(
                recipe=self.recipe,
                ingredient=ingredient_class,
                measure=ingredient["measure"],
                measure_weight=ingredient["measure_weight"]
            )

        self.total_cost = sum([ingredient['measure'] * ingredient['cost'] for ingredient in self.INGREDIENTS])
        self.total_weight = sum(
            [ingredient['measure_weight'] * ingredient['measure'] for ingredient in self.INGREDIENTS])

    def get_response(self):
        """Получение ответа со страницы рецепта"""
        response = self.client.get(reverse('receipt', kwargs={'pk': self.recipe.id}))
        return response

    def test_status_code(self):
        """Проверка кода состояния страницы рецепта"""
        response = self.get_response()
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        """Проверка наличия всех нужных ключей в контексте"""
        response = self.get_response()
        length = sum([1 for key in self.CONTEXT_FIELDS if key in response.context])
        self.assertEqual(length, len(self.CONTEXT_FIELDS))

    def test_total_weight_calculation(self):
        """Проверка расчета общего веса ингредиентов"""
        response = self.get_response()
        self.assertEqual(response.context['total_weight'], self.total_weight)

    def test_total_cost_calculation(self):
        """Проверка расчета общей стоимости ингредиентов"""
        response = self.get_response()
        self.assertEqual(response.context['total_cost'], self.total_cost)

    def tearDown(self):
        self.user.delete()
        self.recipe.delete()
        for ingredient in self.ingredients:
            ingredient.delete()


class TestRecipeEditDeletePermissions(TestCase):
    """Тесты на проверку прав редактирования и удаления рецептов"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        self.recipe = Recipe.objects.create(name="Торт", author=self.user)
        self.client = Client()

    def test_edit_recipe_author(self):
        """Проверка, что автор может редактировать свой рецепт"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('edit_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_recipe_non_author(self):
        """Проверка, что не автор не может редактировать рецепт"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('edit_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe_author(self):
        """Проверка, что автор может удалить свой рецепт"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse('delete_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_delete_recipe_non_author(self):
        """Проверка, что не автор не может удалить рецепт"""
        self.client.login(username="otheruser", password="otherpassword")
        url = reverse('delete_recipe', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.user.delete()
        self.other_user.delete()
        self.recipe.delete()
