from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Unit

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    list_display = ['recipe', 'ingredient']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ["title"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["title", "raw_weight", "cooked_weight", "cost", "unit"]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name", "conversion_to_grams"]
