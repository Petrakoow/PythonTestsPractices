from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Unit(models.Model):
    name = models.CharField(max_length=20)
    conversion_to_grams = models.FloatField(
        validators=[MinValueValidator(0.1, 'Коэффициент преобразования в граммы должен быть не меньше нуля.')]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_unit_per_user')
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яёЁ\s0-9]+$',
                message='Имя не должно содержать спецсимволов'
            )
        ]
    )
    raw_weight = models.FloatField(
        validators=[MinValueValidator(0.1, message='Сырой вес должен быть положительным числом.')]
    )
    cooked_weight = models.FloatField(
        validators=[MinValueValidator(0.1, message='Вес приготовленного продукта должен быть положительным.')]
    )
    cost = models.FloatField(
        validators=[MinValueValidator(0.1, message='Стоимость должна быть больше 0')]
    )
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} (Raw: {self.raw_weight} g, Cooked: {self.cooked_weight} g, Cost: ${self.cost})'

    def save(self, *args, **kwargs):
        if self.unit and not hasattr(self, '_unit_converted'):
            self.raw_weight *= self.unit.conversion_to_grams
            self.cooked_weight *= self.unit.conversion_to_grams
            setattr(self, '_unit_converted', True)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    title = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яёЁ\s0-9]+$',
                message='Рецепт не должен содержать специальных символов.'
            )
        ]
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def total_weight_in_grams(self):
        total_weight = sum(
            recipe_ingredient.weight_in_grams() for recipe_ingredient in self.recipeingredient_set.all()
        )
        return total_weight


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.title}'

    def weight_in_grams(self):
        if self.ingredient.unit:
            return self.ingredient.raw_weight * self.ingredient.unit.conversion_to_grams
        return self.ingredient.raw_weight

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]


