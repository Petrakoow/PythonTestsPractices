from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .constants import INDEX_TEMPLATE_NAME, RECIPE_TEMPLATE_NAME, ABOUT_TEMPLATE_NAME, REGISTER_TEMPLATE_NAME, \
    ADD_RECIPE_TEMPLATE_NAME, ADD_INGREDIENT_TEMPLATE_NAME, MY_RECIPES_TEMPLATE_NAME, \
    ADD_INGREDIENT_TO_RECIPE_TEMPLATE_NAME, EDIT_RECIPE_TEMPLATE_NAME, MANAGE_RECIPIES_TEMPLATE_NAME, \
    DELETE_INGREDIENT_TEMPLATE_NAME, EDIT_INGREDIENT_TEMPLATE_NAME, EDIT_INGREDIENT_FORM_TEMPLATE_NAME, LOGIN_TEMPLATE_NAME
from .forms import UserRegistrationForm, LoginForm, ReceiptForm, IngredientForm, ReceiptIngredientForm, RecipeIngredientsForm
from .utils import check_recipe_existence
from django.http import Http404
from django.contrib.auth import logout, login, authenticate
from .models import Ingredient, RecipeIngredients, Recipe


def check_recipe_author(recipe, user):
    """Проверка, что рецепт принадлежит текущему пользователю"""
    if recipe.author != user:
        raise Http404("У вас нет прав для редактирования этого рецепта.")


def index(request):
    """Main page handler"""
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
        'recipes_len': len(recipes)
    }
    return render(
        request=request,
        template_name=INDEX_TEMPLATE_NAME,
        context=context
    )


def recipe_details(request, pk):
    """Specific recipe details handler"""
    if not check_recipe_existence(pk):
        raise Http404("Рецепт не найден")

    recipe = Recipe.objects.get(pk=pk)
    recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)

    ingredients_list = [
        {
            'id': recipe_ingredient.ingredient.id,
            'name': recipe_ingredient.ingredient.name,
            'measuring': recipe_ingredient.ingredient.measuring,
            'measure': recipe_ingredient.measure,
            'measure_weight': recipe_ingredient.measure_weight,
            'cost': recipe_ingredient.measure *
                    recipe_ingredient.ingredient.cost,

        }
        for recipe_ingredient in recipe_ingredients
    ]

    total_cost = sum([ingredient['cost'] for ingredient in ingredients_list])
    total_weight = sum([ingredient['measure_weight'] * ingredient['measure']
                      for ingredient in ingredients_list])

    context = {
        "recipe": recipe,
        "recipe_ingredients": ingredients_list,
        "total_cost": total_cost,
        "total_weight": total_weight
    }

    return render(request, RECIPE_TEMPLATE_NAME, context)


def about(request):
    """About page handler"""
    return render(request, ABOUT_TEMPLATE_NAME)



def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save() 
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, REGISTER_TEMPLATE_NAME, {'form': form})


def login_view(request):
    form = LoginForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")

    return render(request, LOGIN_TEMPLATE_NAME, {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('main')
    else:
        form = ReceiptForm()
    return render(request, ADD_RECIPE_TEMPLATE_NAME, {'form': form})


@login_required
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = IngredientForm()
    return render(request, ADD_INGREDIENT_TEMPLATE_NAME, {'form': form})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('name')
    return render(request, MY_RECIPES_TEMPLATE_NAME, {'recipes': recipes})


@login_required
def delete_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    check_recipe_author(recipe, request.user)
    if recipe.author == request.user:
        recipe.delete()
    return redirect('my_recipes')


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    check_recipe_author(recipe, request.user)

    if request.method == 'POST':
        form = ReceiptForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('my_recipes')
    else:
        form = ReceiptForm(instance=recipe)

    return render(request, EDIT_RECIPE_TEMPLATE_NAME, {'form': form, 'recipe': recipe})


@login_required
def manage_recipes(request):
    user_recipes = Recipe.objects.filter(author=request.user)

    context = {
        'recipes': user_recipes,
    }
    return render(request, MANAGE_RECIPIES_TEMPLATE_NAME, context)


@login_required
def delete_ingredient(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id, author=request.user)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден или не принадлежит вам")
    if request.method == 'POST':
        ingredient_ids = request.POST.getlist('ingredient_ids')
        RecipeIngredients.objects.filter(recipe=recipe, ingredient_id__in=ingredient_ids).delete()
        return redirect('manage_recipes')

    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    return render(request, DELETE_INGREDIENT_TEMPLATE_NAME, {'recipe': recipe, 'ingredients': ingredients})


@login_required
def edit_ingredient(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id, author=request.user)
    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    check_recipe_author(recipe, request.user)

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient_id')
        return redirect('edit_ingredient_form', recipe_id=recipe_id, ingredient_id=ingredient_id)

    return render(request, EDIT_INGREDIENT_TEMPLATE_NAME, {'recipe': recipe, 'ingredients': ingredients})


@login_required
def add_ingredient_to_recipe_action(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id, author=request.user)
    check_recipe_author(recipe, request.user)

    if request.method == 'POST':
        form = ReceiptIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('manage_recipes')
    else:
        form = ReceiptIngredientForm()

    return render(request, ADD_INGREDIENT_TO_RECIPE_TEMPLATE_NAME, {'form': form, 'recipe': recipe})


@login_required
def edit_ingredient_form(request, recipe_id, ingredient_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    recipe_ingredient = get_object_or_404(RecipeIngredients, recipe=recipe, ingredient_id=ingredient_id)
    check_recipe_author(recipe, request.user)

    if request.method == 'POST':
        form = RecipeIngredientsForm(request.POST, instance=recipe_ingredient)
        if form.is_valid():
            form.save()
            return redirect('manage_recipes')
    else:
        form = RecipeIngredientsForm(instance=recipe_ingredient)

    return render(request, EDIT_INGREDIENT_FORM_TEMPLATE_NAME, {'form': form, 'recipe': recipe})