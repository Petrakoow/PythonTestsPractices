from .models import Ingredient, RecipeIngredients, Recipe


def check_recipe_existence(recipe_id):
    """Is recipe exist"""
    try:
        Recipe.objects.get(id=recipe_id)
        return True
    except Recipe.DoesNotExist:
        return False
