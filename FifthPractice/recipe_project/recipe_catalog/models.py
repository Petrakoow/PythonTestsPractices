from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    conversion_to_grams = models.FloatField(
        validators=[MinValueValidator(0.1, 'Conversion rate must be positive.')]
    )

    def __str__(self):
        return self.name
    
    
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
        validators=[MinValueValidator(0.1, message='Raw weight must be a positive number.')]
    )
    cooked_weight = models.FloatField(
        validators=[MinValueValidator(0.1, message='Cooked weight must be a positive number.')]
    )
    cost = models.FloatField(
        validators=[MinValueValidator(0.1, message='Cost must be a positive number.')]
    )
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

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
                regex=r'^[A-Za-zА-Яа-яёЁ\s]+$',
                message='Title should be a string value.'
            )
        ]
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

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
