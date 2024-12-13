from django.test import TestCase
from recipe_catalog.models import Unit, Ingredient, Recipe, RecipeIngredient
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User

class TestIngredientAndRecipeCreation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20, author=self.user)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250, author=self.user)

    def test_ingredient_creation_with_default_unit(self):
        ingredient = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        self.assertEqual(ingredient.title, "Мука")
        self.assertEqual(ingredient.raw_weight, 100)
        self.assertEqual(ingredient.cooked_weight, 90)
        self.assertEqual(ingredient.cost, 50)
        self.assertEqual(ingredient.author, self.user)

    def test_ingredient_creation_with_unit_conversion(self):
        ingredient = Ingredient.objects.create(
            title="Йогурт", raw_weight=200, cooked_weight=180, cost=50, unit=self.spoon, author=self.user
        )
        ingredient.save()  
        self.assertEqual(ingredient.raw_weight, 200 * 20)  
        self.assertEqual(ingredient.cooked_weight, 180 * 20)
        self.assertEqual(ingredient.author, self.user)

    def test_recipe_creation(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40, author=self.user
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.", author=self.user)
        recipe.ingredients.set([ingredient_flour, ingredient_sugar])

        self.assertEqual(recipe.title, "Парфе с ягодами и сливками.")
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(RecipeIngredient.objects.count(), 2)
        self.assertEqual(recipe.author, self.user)

    def test_recipe_total_weight_calculation(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40, author=self.user
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.", author=self.user)
        recipe.ingredients.set([ingredient_flour, ingredient_sugar])

        total_weight = recipe.total_weight_in_grams()
        self.assertEqual(total_weight, 180)

    def test_unique_recipe_ingredient_constraint(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.", author=self.user)
        recipe.ingredients.set([ingredient_flour])

        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient_flour)

    def test_recipe_creation_with_ingredients(self):
        recipe_data = {
            "title": "Ерундопель - Запечённое лакомство с секретом.",
            "ingredients_list": [
                ("Творог", 250, 230, 180),
                ("Сметана", 100, 95, 80),
                ("Яйца", 2, 2, 50),
                ("Сахар", 80, 80, 40),
                ("Мука", 100, 100, 90),
                ("Ванилин", 1, 1, 5)
            ]
        }
        recipe = Recipe.objects.create(title=recipe_data['title'], author=self.user)
        ingredients = [
            Ingredient.objects.create(
                title=ingredient[0], raw_weight=ingredient[1], cooked_weight=ingredient[2], cost=ingredient[3], author=self.user
            ) for ingredient in recipe_data['ingredients_list']
        ]
        recipe.ingredients.add(*ingredients)

        self.assertEqual(recipe.ingredients.count(), 6)

        total_weight = recipe.total_weight_in_grams()
        expected_weight = sum(ingredient[1] for ingredient in recipe_data['ingredients_list'])
        self.assertEqual(total_weight, expected_weight)


class TestIngredientListOrdering(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20, author=self.user)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250, author=self.user)
        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        self.ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40, author=self.user
        )
        self.ingredient_yogurt = Ingredient.objects.create(
            title="Йогурт", raw_weight=200, cooked_weight=180, cost=50, unit=self.spoon, author=self.user
        )
        self.recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.", author=self.user)
        self.recipe.ingredients.set([self.ingredient_flour, self.ingredient_sugar, self.ingredient_yogurt])

    def test_ingredients_are_sorted_in_alphabetical_order(self):
        url = reverse('recipe-information', args=[self.recipe.pk])
        response = self.client.get(url)
        ingredients = response.context['recipe_ingredients']
        ingredient_titles = [ingredient['name'] for ingredient in ingredients]
        self.assertEqual(ingredient_titles, sorted(ingredient_titles))


class TestUniqueRecipeIngredientConstraintError(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50, author=self.user
        )
        self.recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.", author=self.user)
        self.recipe.ingredients.set([self.ingredient_flour])

    def test_adding_duplicate_ingredient_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient_flour)

class TestIngredientValidationErrors(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_create_ingredient_with_invalid_raw_weight(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=0.05, cooked_weight=90, cost=50, author=self.user
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean()

    def test_create_ingredient_with_invalid_cooked_weight(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=100, cooked_weight=0.05, cost=50, author=self.user
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean()

    def test_create_ingredient_with_invalid_cost(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=100, cooked_weight=90, cost=0.05, author=self.user
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean()
