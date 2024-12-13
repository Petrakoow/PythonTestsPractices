from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from recipe_catalog.models import Recipe, RecipeIngredient
from recipe_catalog.forms import RecipeForm, RecipeIngredientForm
from recipe_catalog.constants import templates
from django.contrib import messages

def check_recipe_author(recipe, user):
    if recipe.author != user:
        raise Http404("У вас нет прав для редактирования этого рецепта.")

def recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    
    ingredients_list = [
        {
            'id': recipe_ingredient.ingredient.id,
            'name': recipe_ingredient.ingredient.title,
            'raw_weight': recipe_ingredient.ingredient.raw_weight,
            'cooked_weight': recipe_ingredient.ingredient.cooked_weight,
            'cost': recipe_ingredient.ingredient.cost,
        }
        for recipe_ingredient in recipe_ingredients
    ]

    ingredients_list.sort(key=lambda x: x['name'])

    total_cost = sum([ingredient['cost'] for ingredient in ingredients_list])
    total_weight = sum([ingredient['raw_weight'] for ingredient in ingredients_list])

    context = {
        "recipe": recipe,
        "recipe_ingredients": ingredients_list,
        "total_cost": total_cost,
        "total_weight": total_weight
    }

    return render(request, templates['recipe_page'], context)

@login_required
def manage_recipes(request):
    user_recipes = Recipe.objects.filter(author=request.user)

    context = {
        'recipes': user_recipes,
    }
    return render(request, templates['manage_recipes_page'], context)

@login_required
def your_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, templates['your_recipes_page'], {'recipes': recipes})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('recipe-information', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, templates['add_recipe_page'], {'form': form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт обновлён.')
            return redirect('your-recipes')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, templates['edit_recipe_page'], {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Рецепт удалён.')
        return redirect('your-recipes')
    return render(request, templates['delete_recipe_page'], {'recipe': recipe})


@login_required
def edit_ingredient_in_recipe(request, recipe_id, ingredient_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    recipe_ingredient = get_object_or_404(RecipeIngredient, recipe=recipe, ingredient_id=ingredient_id)

    check_recipe_author(request, request.user)

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST, instance=recipe_ingredient)
        if form.is_valid():
            form.save()  
            return redirect('recipe_details', pk=recipe.pk)
    else:
        form = RecipeIngredientForm(instance=recipe_ingredient)

    return render(
        request,
        templates['edit_ingredient_form_page'],
        {'form': form, 'recipe': recipe, 'ingredient': recipe_ingredient}
    )
