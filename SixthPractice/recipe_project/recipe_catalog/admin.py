from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Unit


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('ingredient',) 


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'raw_weight', 'cooked_weight', 'cost', 'unit', 'author') 
    search_fields = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title',)
    inlines = [RecipeIngredientInline]  


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')  

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'conversion_to_grams', 'author')
    search_fields = ('name',)
    list_filter = ('author',)
