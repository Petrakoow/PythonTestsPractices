from django.shortcuts import render
from django.http import Http404
from .constants import recipes

def about(request):
    return render(request, 'recipe_catalog/about.html')

def index(request):
    return render(
        request=request,
        template_name='recipe_catalog/index.html',
        context={'recipes': recipes}
    )

def recipe_detail(request, pk):
    recipe = next((r for r in recipes if r.id == pk), None)
    if recipe is None:
        raise Http404("Recipe does not exist")
    total_raw_weight = recipe.calc_weight(raw=True, portions=1)
    total_cooked_weight = recipe.calc_weight(raw=False, portions=1)
    print(total_cooked_weight)
    return render(
        request=request,
        template_name='recipe_catalog/recipe.html',
        context={
            'recipe': recipe,
            'total_raw_weight': total_raw_weight,
            'total_cooked_weight': total_cooked_weight,
        }
    )
