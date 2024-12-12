from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Ingredient, RecipeIngredients, Recipe


class TestDbCreation(TestCase):
    """Тесты успешного создания в базе данных"""

    INGREDIENT_NAME = 'Тестовый ингредиент'
    INGREDIENT_MEASURING = 'грамм'
    INGREDIENT_COST = 10
    INGREDIENT_MEASURE = 100
    INGREDIENT_MEASURE_WEIGHT = 1
    RECIPE_NAME = 'Тестовый рецепт'
    USER_NAME = "testuser"
    USER_PASSWORD = "testpassword"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=cls.USER_NAME, password=cls.USER_PASSWORD)
        cls.ingredient_test = Ingredient.objects.create(
            name=cls.INGREDIENT_NAME,
            measuring=cls.INGREDIENT_MEASURING,
            cost=cls.INGREDIENT_COST,
        )
        cls.recipe_test = Recipe.objects.create(
            name=cls.RECIPE_NAME,
            author=cls.user,
        )
        cls.recipe_ingredient_test = RecipeIngredients.objects.create(
            recipe=cls.recipe_test,
            ingredient=cls.ingredient_test,
            measure=cls.INGREDIENT_MEASURE,
            measure_weight=cls.INGREDIENT_MEASURE_WEIGHT
        )

    def test_validate_ingredient_name(self):
        """Проверка имени ингредиента"""
        ingredient = Ingredient.objects.get(id=self.ingredient_test.id)
        self.assertEqual(ingredient.name, self.INGREDIENT_NAME)

    def test_validate_ingredient_measuring(self):
        """Проверка вида измерения ингредиента"""
        ingredient = Ingredient.objects.get(id=self.ingredient_test.id)
        self.assertEqual(ingredient.measuring, self.INGREDIENT_MEASURING)

    def test_validate_ingredient_cost(self):
        """Проверка стоимости ингредиента"""
        ingredient = Ingredient.objects.get(id=self.ingredient_test.id)
        self.assertEqual(ingredient.cost, self.INGREDIENT_COST)

    def test_validate_recipe_name(self):
        """Проверка имени рецепта"""
        recipe = Recipe.objects.get(id=self.recipe_test.id)
        self.assertEqual(recipe.name, self.RECIPE_NAME)

    def test_validate_recipe_ingredients_count(self):
        """Проверка количества ингредиентов в рецепте"""
        recipe = Recipe.objects.get(id=self.recipe_test.id)
        self.assertEqual(recipe.ingredients.count(), 1)

    def test_validate_ingredient_measure(self):
        """Проверка измерения ингредиента в рецепте"""
        recipe = Recipe.objects.get(id=self.recipe_test.id)
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        self.assertEqual(recipe_ingredients[0].measure, self.INGREDIENT_MEASURE)

    def test_validate_ingredient_measure_weight(self):
        """Проверка веса ингредиента в рецепте"""
        recipe = Recipe.objects.get(id=self.recipe_test.id)
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        self.assertEqual(recipe_ingredients[0].measure_weight, self.INGREDIENT_MEASURE_WEIGHT)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.ingredient_test.delete()
        cls.recipe_test.delete()
        cls.recipe_ingredient_test.delete()


class TestErrors(TestCase):
    """Тесты на ошибки валидации"""

    INGREDIENT_NAME = 'TEST'
    INGREDIENT_MEASURING = 'грамм'
    INGREDIENT_COST = 10
    SUP_INGREDIENT_COST = 15
    USER_NAME = "testuser"
    USER_PASSWORD = "testpassword"

    def test_ingredient_name_unique(self):
        """Проверка уникальности имени ингредиента"""
        Ingredient.objects.create(
            name=self.INGREDIENT_NAME,
            measuring=self.INGREDIENT_MEASURING,
            cost=self.INGREDIENT_COST,
        )
        with self.assertRaises(ValidationError):
            ingredient = Ingredient(
                name=self.INGREDIENT_NAME,
                measuring=self.INGREDIENT_MEASURING,
                cost=self.SUP_INGREDIENT_COST
            )
            ingredient.full_clean()

    def test_ingredient_cost_min_value(self):
        """Проверка минимального значения для стоимости ингредиента"""
        with self.assertRaises(ValidationError):
            ingredient = Ingredient(
                name=self.INGREDIENT_NAME,
                measuring=self.INGREDIENT_MEASURING,
                cost=0.0
            )
            ingredient.full_clean()

    def test_recipe_name_unique(self):
        """Проверка уникальности имени рецепта"""
        user = User.objects.create_user(username=self.USER_NAME, password=self.USER_PASSWORD)
        Recipe.objects.create(name="Cake", author=user)
        with self.assertRaises(ValidationError):
            recipe = Recipe(name="Cake", author=user)
            recipe.full_clean()


class TestRecipeIngredientsError(TestCase):
    """Тесты на ошибки при добавлении ингредиентов в рецепт"""
    USER_NAME = "testuser"
    USER_PASSWORD = "testpassword"

    def setUp(self):
        """Создаем тестовые данные для ингредиента и рецепта"""
        self.user = User.objects.create_user(username=self.USER_NAME, password=self.USER_PASSWORD)
        self.ingredient = Ingredient.objects.create(name="Тест", measuring="грамм", cost=2.0)
        self.recipe = Recipe.objects.create(name="Тест", author=self.user)

    def test_recipe_ingredient_unique_together(self):
        """Проверка уникальности пары рецепт-ингредиент"""
        RecipeIngredients.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            measure=50,
            measure_weight=100
        )
        with self.assertRaises(ValidationError):
            duplicate_entry = RecipeIngredients(
                recipe=self.recipe,
                ingredient=self.ingredient,
                measure=30,
                measure_weight=50
            )
            duplicate_entry.full_clean()

    def test_recipe_ingredient_measure_min_value(self):
        """Проверка минимального значения для количества ингредиента"""
        with self.assertRaises(ValidationError):
            recipe_ingredient = RecipeIngredients(
                recipe=self.recipe,
                ingredient=self.ingredient,
                measure=0,
                measure_weight=100
            )
            recipe_ingredient.full_clean()

    def tearDown(self):
        self.user.delete()
        self.ingredient.delete()
        self.recipe.delete()
