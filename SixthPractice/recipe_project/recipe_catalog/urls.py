from django.urls import path
from .views import about, index, recipe_details, registration_view, \
login_view, logout_view, add_recipe, your_recipes, \
add_ingredient, delete_recipe, edit_recipe, manage_recipes, \
edit_ingredient, add_ingredient_to_recipe, \
edit_ingredient_form, manage_units, add_unit, edit_unit, delete_unit, \
edit_ingredient_element, delete_ingredient_element, manage_ingredients

urlpatterns = [
    path('', index, name='main'),
    path('recipe-information/<int:pk>/', recipe_details, name='recipe-information'),
    path('about-us', about, name='about-us'),
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),

    path('your-recipes/', your_recipes, name='your-recipes'),
    path('manage-recipes-unit/', manage_recipes, name='manage-recipes-unit'),
    path('add-recipe/', add_recipe, name='add-recipe'),
    path('delete-recipe/<int:pk>/', delete_recipe, name='delete-recipe'),
    path('edit-recipe/<int:pk>/', edit_recipe, name='edit-recipe'),

    path('add-ingredient/', add_ingredient, name='add-ingredient'),
    
    path('manage-recipes/', manage_recipes, name='manage-recipes'),
    path('manage-recipes/edit-ingredient/<int:pk>/', edit_ingredient, name='edit-ingredient'),
    path('manage-recipes/add-ingredient-to-recipe/<int:pk>/', add_ingredient_to_recipe, name='add-ingredient-to-recipe'),
    path('manage-recipes/edit-ingredient-form/<int:recipe_id>/<int:ingredient_id>/', edit_ingredient_form, name='edit_ingredient_form'),

    path('manage-units/', manage_units, name='manage-units'),
    path('add-unit/', add_unit, name='add-unit'),
    path('edit-unit/<int:pk>/', edit_unit, name='edit-unit'),
    path('delete-unit/<int:pk>/', delete_unit, name='delete-unit'),

    path('manage-ingredients/', manage_ingredients, name='manage-ingredients'),
    path('manage-ingredients/delete-ingredient-element/<int:pk>/', delete_ingredient_element, name='delete-ingredient-element'),
    path('manage-ingredients/edit-ingredient-element/<int:pk>/', edit_ingredient_element, name='edit-ingredient-element'),

]
