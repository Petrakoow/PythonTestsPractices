from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render(
        request=request,
        template_name='recipe_catalog/index.html',
        context={'recipes': recipes}
    )


def about(request):
    return render(
        request=request,
        template_name='recipe_catalog/about.html'
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    total_raw_weight = recipe.ingredients.aggregate(total=Sum('raw_weight'))['total']
    total_cooked_weight = recipe.ingredients.aggregate(total=Sum('cooked_weight'))['total']
    total_cost = recipe.ingredients.aggregate(total=Sum('cost'))['total']
    
    return render(
        request=request,
        template_name='recipe_catalog/recipe.html',
        context={
            'recipe': recipe,
            'total_raw_weight': total_raw_weight,
            'total_cooked_weight': total_cooked_weight,
            'total_cost': total_cost,
        }
    )
