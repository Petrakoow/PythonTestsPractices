### Практическая работа №3 (Часть 2) - Django проект для управления рецептами

В этой части практической работы создается функциональность для управления рецептами и ингредиентами, включая модели, настройки панели администратора и отображение данных на страницах.

### Описание задания
1. **Создание моделей**: В этом задании добавляются модели для рецепта и ингредиента, чтобы хранить информацию о названиях, весе (сырьё и готовое) и стоимости ингредиентов.
2. **Настройка панели администратора**: Настроена панель администратора Django для удобного управления рецептами и ингредиентами.
3. **Изменение вьюшек**: Изменены представления для отображения данных рецептов и ингредиентов на страницах.

#### Рекомендации:
- **Проектирование моделей**: Важно продумать обязательные атрибуты и связи между моделями перед заполнением базы данных. Изменение структуры БД с данными может быть трудоемким.
- **Презентация работы**: Особое внимание следует уделить внешнему виду страниц. Данные рецептов и ингредиентов должны отображаться аккуратно и организованно.

---

### Основные этапы выполнения работы

1. **Изучение ORM модели**: Изучена работа с Django ORM для создания моделей и взаимодействия с базой данных.
2. **Создание моделей и миграции**: Модели для рецептов и ингредиентов созданы с нужными атрибутами, после чего выполнены миграции.
3. **Настройка панели администратора**: Добавлены настройки панели администратора для работы с моделями.

---

### Код

#### Админка

Панель администратора настроена для управления рецептами и ингредиентами с помощью связующей модели `RecipeIngredient`, которая позволяет задавать множество ингредиентов для каждого рецепта.

```python
from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ["title"]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["title", "raw_weight", "cooked_weight", "cost"]
```

#### Модели

Включены модели для `Recipe`, `Ingredient` и `RecipeIngredient`. Модель `RecipeIngredient` используется как промежуточная для связи многие ко многим между рецептами и ингредиентами.

```python
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Ingredient(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(regex=r'^[A-Za-zА-Яа-яёЁ\s]+$', message='Name should be a string value.')
        ]
    )
    raw_weight = models.FloatField(validators=[MinValueValidator(0.1, 'Raw weight must be a positive number.')])
    cooked_weight = models.FloatField(validators=[MinValueValidator(0.1, 'Cooked weight must be a positive number.')])
    cost = models.FloatField(validators=[MinValueValidator(0.1, 'Cost must be a positive number.')])

    def __str__(self):
        return f'{self.title} (Raw: {self.raw_weight} g, Cooked: {self.cooked_weight} g, Cost: ${self.cost})'

class Recipe(models.Model):
    title = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=r'^[A-Za-zА-Яа-яёЁ\s]+$', message='Title should be a string value.')
        ]
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]
```

#### Вьюшки

Добавлены три представления для отображения списка рецептов, детальной информации о рецепте и страницы «О компании».

```python
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_catalog/index.html', {'recipes': recipes})

def about(request):
    return render(request, 'recipe_catalog/about.html')

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    total_raw_weight = recipe.ingredients.aggregate(total=Sum('raw_weight'))['total']
    total_cooked_weight = recipe.ingredients.aggregate(total=Sum('cooked_weight'))['total']
    total_cost = recipe.ingredients.aggregate(total=Sum('cost'))['total']
    
    return render(
        request,
        'recipe_catalog/recipe_detail.html',
        {
            'recipe': recipe,
            'total_raw_weight': total_raw_weight,
            'total_cooked_weight': total_cooked_weight,
            'total_cost': total_cost,
        }
    )
```


### Заключение
Эта часть практической работы демонстрирует основные навыки создания и настройки моделей Django, панели администратора и представлений для отображения данных.