from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from recipe_catalog.models import Ingredient, Recipe, RecipeIngredient, Unit
from recipe_catalog.forms import IngredientForm, RecipeIngredientForm
from recipe_catalog.constants import templates
from django.contrib import messages

@login_required
def add_ingredient(request):
    print(f'Current user: {request.user}')
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.author = request.user
            ingredient.save()
            return redirect('manage-recipes')
    else:
        form = IngredientForm()

    return render(request, templates['add_ingredient_page'], {'form': form})


@login_required
def manage_ingredients(request):
    user_ingredients = Ingredient.objects.filter(unit__author=request.user)
    return render(request, templates['manage_ingredients_page'], {'ingredients': user_ingredients})


@login_required
def edit_ingredient(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    
    if request.method == 'POST':
        selected_ingredient_id = request.POST.get('ingredient_id')
        if selected_ingredient_id:
            ingredient = get_object_or_404(Ingredient, pk=selected_ingredient_id)
            return redirect('edit_ingredient_form', recipe_id=recipe.id, ingredient_id=ingredient.id)

    return render(request, templates['edit_ingredient_page'], {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients,
        'selected_ingredient_id': request.POST.get('ingredient_id')
    })


@login_required
def add_ingredient_to_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        
        if form.is_valid():
            ingredient = form.cleaned_data.get('ingredient')
            
            if ingredient is None:
                messages.error(request, 'Please select a valid ingredient.')
                return redirect('add-ingredient-to-recipe', pk=recipe.pk)
            
            existing_recipe_ingredient = RecipeIngredient.objects.filter(
                recipe=recipe, ingredient=ingredient
            ).first()

            if existing_recipe_ingredient:
                messages.error(request, 'This ingredient is already added to the recipe.')
            else:
                recipe_ingredient = form.save(commit=False)
                recipe_ingredient.recipe = recipe
                recipe_ingredient.save()
                messages.success(request, 'Ingredient added successfully.')
                
            return redirect('add-ingredient-to-recipe', pk=recipe.pk)
    else:
        form = RecipeIngredientForm()

    return render(request, templates['add_ingredient_to_recipe_page'], {'form': form, 'recipe': recipe})


@login_required
def edit_ingredient_form(request, recipe_id, ingredient_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    recipe_ingredient = get_object_or_404(RecipeIngredient, recipe=recipe, ingredient_id=ingredient_id)

    if recipe.author != request.user:
        messages.error(request, "У вас нету доступа к этому рецепту.")
        return redirect('manage-recipes')

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST, instance=recipe_ingredient)
        if form.is_valid():
            ingredient = form.cleaned_data['ingredient']
            if ingredient is None:
                recipe_ingredient.delete()
                messages.success(request, "Ингредиент удалён из рецепта!")
            else:
                form.save()
                messages.success(request, "Ингредиент успешно обновлен!")
            return redirect('recipe-information', pk=recipe_id)  
        else:
            messages.error(request, "Произошла ошибка при обновлении ингредиента.")
    else:
        form = RecipeIngredientForm(instance=recipe_ingredient)

    return render(request, templates['edit_ingredient_form_page'], {'form': form, 'recipe': recipe})

@login_required
def manage_ingredients(request):
    ingredients = Ingredient.objects.filter(author=request.user)
    return render(request, templates['manage_ingredients_page'], {'ingredients': ingredients})


@login_required
def delete_ingredient_element(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk, author=request.user)
    if request.method == 'POST':
        ingredient.delete()
        messages.success(request, 'Ингредиент удалён.')
        return redirect('manage-ingredients')
    return render(request, templates['delete_ingredient_element_page'], {'ingredient': ingredient})

@login_required
def edit_ingredient_element(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk, author=request.user)

    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ингредиент обновлён.')
            return redirect('manage-ingredients')
    else:
        form = IngredientForm(instance=ingredient)

    return render(request, templates['edit_ingredient_element_page'], {'form': form, 'ingredient': ingredient})
