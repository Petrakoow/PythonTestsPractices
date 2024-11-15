from django.test import TestCase
from recipe_catalog.models import Unit, Ingredient, Recipe, RecipeIngredient
from django.db import IntegrityError


class TestIngredientAndRecipeCreation(TestCase):
    def setUp(self):
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250)

    def test_ingredient_creation_with_default_unit(self):
        ingredient = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        self.assertEqual(ingredient.title, "Мука")
        self.assertEqual(ingredient.raw_weight, 100)
        self.assertEqual(ingredient.cooked_weight, 90)
        self.assertEqual(ingredient.cost, 50)

    def test_ingredient_creation_with_unit_conversion(self):
        ingredient = Ingredient.objects.create(
            title="Йогурт", raw_weight=200, cooked_weight=180, cost=50, unit=self.spoon
        )
        ingredient.save()
        self.assertEqual(ingredient.raw_weight, 200 * 20)
        self.assertEqual(ingredient.cooked_weight, 180 * 20)

    def test_recipe_creation(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.")
        recipe.ingredients.set([ingredient_flour, ingredient_sugar])

        self.assertEqual(recipe.title, "Парфе с ягодами и сливками.")
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(RecipeIngredient.objects.count(), 2)

    def test_recipe_total_weight_calculation(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.")
        recipe.ingredients.set([ingredient_flour, ingredient_sugar])

        total_weight = recipe.total_weight_in_grams()
        self.assertEqual(total_weight, 180)

    def test_unique_recipe_ingredient_constraint(self):
        ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.")
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
        recipe = Recipe.objects.create(title=recipe_data['title'])
        ingredients = [
            Ingredient.objects.create(
                title=ingredient[0], raw_weight=ingredient[1], cooked_weight=ingredient[2], cost=ingredient[3]
            ) for ingredient in recipe_data['ingredients_list']
        ]
        recipe.ingredients.add(*ingredients)

        self.assertEqual(recipe.ingredients.count(), 6)

        total_weight = recipe.total_weight_in_grams()
        expected_weight = sum(ingredient[1] for ingredient in recipe_data['ingredients_list'])
        self.assertEqual(total_weight, expected_weight)
