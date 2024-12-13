from django.shortcuts import render
from recipe_catalog.models import Recipe
from recipe_catalog.constants import templates

def index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
        'recipes_len': len(recipes)
    }
    return render(
        request=request,
        template_name=templates['index_page'],
        context=context
    )

def about(request):
    return render(request, templates['about_page'])