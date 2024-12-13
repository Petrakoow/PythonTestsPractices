class RecipeCatalogTemplates:
    def __init__(self):
        self.templates = {
            'index_page': 'recipe_catalog/index.html',
            'recipe_page': 'recipe_catalog/recipe-information.html',
            'about_page': 'recipe_catalog/about-us.html',
            'registration_page': 'recipe_catalog/registration.html',
            'login_page': 'recipe_catalog/login.html',
            'add_recipe_page': 'recipe_catalog/add-recipe.html',
            'add_ingredient_page': 'recipe_catalog/add-ingredient.html',
            'your_recipes_page': 'recipe_catalog/your-recipes.html',
            'add_ingredient_to_recipe_page': 'recipe_catalog/add-ingredient-to-recipe.html',
            'edit_recipe_page': 'recipe_catalog/edit-recipe.html',
            'delete_recipe_page': 'recipe_catalog/delete-recipe.html',
            'manage_recipes_page': 'recipe_catalog/manage-recipes.html',
            'delete_ingredient_page': 'recipe_catalog/delete-ingredient.html',
            'edit_ingredient_page': 'recipe_catalog/edit-ingredient.html',
            'edit_ingredient_form_page': 'recipe_catalog/edit-ingredient-form.html',
            'manage_units_page': 'recipe_catalog/manage-units.html',
            'edit_units_page': 'recipe_catalog/edit-unit.html',
            'add_units_page': 'recipe_catalog/add-unit.html',
            'delete_units_page': 'recipe_catalog/delete-unit.html',
            'manage_ingredients_page': 'recipe_catalog/manage-ingredients.html',
            'delete_ingredient_element_page': 'recipe_catalog/delete-ingredient-element.html',
            'edit_ingredient_element_page': 'recipe_catalog/edit-ingredient-element.html',

        }

    def __getitem__(self, key):
        return self.templates.get(key)

templates = RecipeCatalogTemplates()
