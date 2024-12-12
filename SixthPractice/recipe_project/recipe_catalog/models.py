from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    """Ingredient model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    measuring = models.CharField(max_length=255)
    cost = models.FloatField(validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Recipe = Ingredient model"""
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.IntegerField(validators=[MinValueValidator(1)])
    measure_weight = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('recipe', 'ingredient')
