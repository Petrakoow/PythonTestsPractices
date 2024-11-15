from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Ingredient(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яёЁ\s]+$',
                message='Name should be a string value.'
            )
        ]
    )
    raw_weight = models.FloatField(
        validators=[
            MinValueValidator(
                limit_value=0.1,
                message='Raw weight must be a positive number.'
            )
        ]
    )
    cooked_weight = models.FloatField(
        validators=[
            MinValueValidator(
                limit_value=0.1,
                message='Cooked weight must be a positive number.'
            )
        ]
    )
    cost = models.FloatField(
        validators=[
            MinValueValidator(
                limit_value=0.1,
                message='Cost must be a positive number.'
            )
        ]
    )

    def __str__(self):
        return f'{self.title} (Raw: {self.raw_weight} g, Cooked: {self.cooked_weight} g, Cost: ${self.cost})'


class Recipe(models.Model):
    title = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яёЁ\s]+$',
                message='Title should be a string value.'
            )
        ]
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
