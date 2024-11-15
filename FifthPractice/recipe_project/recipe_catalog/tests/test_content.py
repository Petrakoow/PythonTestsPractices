from django.test import TestCase
from recipe_catalog.models import Unit, Ingredient, Recipe, RecipeIngredient
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse


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


class TestIngredientListOrdering(TestCase):
    def setUp(self):
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250)
        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        self.ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=80, cooked_weight=75, cost=40
        )
        self.ingredient_yogurt = Ingredient.objects.create(
            title="Йогурт", raw_weight=200, cooked_weight=180, cost=50, unit=self.spoon
        )
        self.recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.")
        self.recipe.ingredients.set([self.ingredient_flour, self.ingredient_sugar, self.ingredient_yogurt])

    def test_ingredients_are_sorted_in_alphabetical_order(self):
        url = reverse('recipe_detail', args=[self.recipe.pk])
        response = self.client.get(url)
        ingredients = response.context['ingredients']
        ingredient_titles = [ingredient.title for ingredient in ingredients]
        self.assertEqual(ingredient_titles, sorted(ingredient_titles))



class TestRecipeWeightWithDifferentUnits(TestCase):
    def setUp(self):
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250)

        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        self.ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=200, cooked_weight=190, cost=60, unit=self.glass
        )
        self.recipe = Recipe.objects.create(title="Торт")
        self.recipe.ingredients.set([self.ingredient_flour, self.ingredient_sugar])

    def test_recipe_weight_with_mixed_units(self):
        url = reverse('recipe_detail', args=[self.recipe.pk])
        response = self.client.get(url)
        total_raw_weight = response.context['total_raw_weight']
        total_cooked_weight = response.context['total_cooked_weight']

        expected_raw_weight = 100 + (200 * 250)
        expected_cooked_weight = 90 + (190 * 250)

        self.assertEqual(total_raw_weight, expected_raw_weight)
        self.assertEqual(total_cooked_weight, expected_cooked_weight)

class TestUniqueRecipeIngredientConstraintError(TestCase):
    def setUp(self):
        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        self.recipe = Recipe.objects.create(title="Парфе с ягодами и сливками.")
        self.recipe.ingredients.set([self.ingredient_flour])

    def test_adding_duplicate_ingredient_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient_flour)

class TestIngredientValidationErrors(TestCase):
    def test_create_ingredient_with_invalid_raw_weight(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=0.05, cooked_weight=90, cost=50
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean() 

    def test_create_ingredient_with_invalid_cooked_weight(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=100, cooked_weight=0.05, cost=50
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean()  

    def test_create_ingredient_with_invalid_cost(self):
        ingredient = Ingredient(
            title="Мука", raw_weight=100, cooked_weight=90, cost=0.05
        )
        with self.assertRaises(ValidationError):
            ingredient.full_clean() 

class TestRecipeWeightOnDetailPage(TestCase):
    def setUp(self):
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250)

        self.ingredient_flour = Ingredient.objects.create(
            title="Мука", raw_weight=100, cooked_weight=90, cost=50
        )
        self.ingredient_sugar = Ingredient.objects.create(
            title="Сахар", raw_weight=200, cooked_weight=190, cost=60, unit=self.glass
        )

        self.recipe = Recipe.objects.create(title="Торт")
        self.recipe.ingredients.set([self.ingredient_flour, self.ingredient_sugar])

    def test_recipe_total_weight_on_detail_page(self):
        url = reverse('recipe_detail', args=[self.recipe.pk])
        response = self.client.get(url)

        expected_raw_weight = self.ingredient_flour.raw_weight + self.ingredient_sugar.raw_weight
        expected_cooked_weight = self.ingredient_flour.cooked_weight + self.ingredient_sugar.cooked_weight

        total_raw_weight = response.context['total_raw_weight']
        total_cooked_weight = response.context['total_cooked_weight']

        self.assertEqual(total_raw_weight, expected_raw_weight)
        self.assertEqual(total_cooked_weight, expected_cooked_weight)