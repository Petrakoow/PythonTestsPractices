### Практическая работа №3 (Часть 2) - Django проект для управления рецептами

В этой части практической работы создается функциональность для управления рецептами и ингредиентами, включая модели, настройки панели администратора и отображение данных на страницах.

### Описание задания
1. **Создание моделей**: В этом задании добавляются модели для рецепта и ингредиента, чтобы хранить информацию о названиях, весе (сырьё и готовое) и стоимости ингредиентов.
2. **Настройка панели администратора**: Настроена панель администратора Django для удобного управления рецептами и ингредиентами.
3. **Изменение вьюшек**: Изменены представления для отображения данных рецептов и ингредиентов на страницах.

#### Рекомендации:
- **Проектирование моделей**: Важно продумать обязательные атрибуты и связи между моделями перед заполнением базы данных. Изменение структуры БД с данными может быть трудоемким.
- **Презентация работы**: Особое внимание следует уделить внешнему виду страниц. Данные рецептов и ингредиентов должны отображаться аккуратно и организованно.

## ORM в Django
**ORM (Object-Relational Mapping)** — это способ взаимодействия с базой данных через объекты. В Django ORM позволяет работать с данными как с Python-объектами, абстрагируя разработчика от специфики SQL-запросов. Это делает код более чистым и позволяет проще изменять структуру базы данных, не изменяя логику приложения.

В данном проекте для работы с данными о рецептах и ингредиентах создаются модели `Recipe` и `Ingredient`, которые представляют таблицы в базе данных. ORM позволяет легко добавлять, изменять, удалять и получать данные из этих таблиц.

## Модели и миграции
Модели в Django представляют таблицы в базе данных. Мы создаем классы для представления каждой таблицы (например, `Recipe`, `Ingredient` и `RecipeIngredient`). Каждое поле в модели соответствует столбцу в таблице базы данных, а каждый экземпляр модели — строке в этой таблице.

### Как добавить модель
1. Определите класс в файле `models.py`, указав нужные поля.
2. Каждое поле должно быть экземпляром одного из классов полей Django (`CharField`, `FloatField`, `ForeignKey` и т.д.) и определяет, какие данные будут храниться в этом столбце.
3. Установите валидаторы для полей, если хотите ограничить вводимые данные (например, только положительные значения веса и стоимости).

### Миграции
Миграции в Django — это механизм для синхронизации моделей с базой данных. После создания или изменения модели необходимо создать и применить миграции:
- Команда `python manage.py makemigrations` создаёт файл миграции, который содержит инструкции для базы данных на основании изменений в моделях.
- Команда `python manage.py migrate` применяет миграции к базе данных, добавляя или изменяя таблицы и столбцы согласно модели.

Миграции помогают избегать ошибок и сохраняют целостность базы данных, поскольку они автоматически адаптируют структуру базы данных к изменениям в моделях.

---

### Основные этапы выполнения работы

1. **Изучение ORM модели**: Изучена работа с Django ORM для создания моделей и взаимодействия с базой данных.
2. **Создание моделей и миграции**: Модели для рецептов и ингредиентов созданы с нужными атрибутами, после чего выполнены миграции.
3. **Настройка панели администратора**: Добавлены настройки панели администратора для работы с моделями.

---

### Код

#### Admin

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

#### Models

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

#### Views

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

## Описание полей

### Модель `Ingredient`
- **title** — Название ингредиента. Используется ограничение на ввод текста, чтобы разрешить только алфавитные символы (русские или латинские).
- **raw_weight** — Вес ингредиента до приготовления. Валидатор ограничивает значение, чтобы оно было больше 0.
- **cooked_weight** — Вес ингредиента после приготовления. Также ограничивается положительными значениями.
- **cost** — Стоимость ингредиента. Введено ограничение на положительное значение.

### Модель `Recipe`
- **title** — Название рецепта с валидатором, допускающим только буквы.
- **ingredients** — Поле для связи "многие ко многим" с моделью `Ingredient` через промежуточную модель `RecipeIngredient`. Это позволяет создавать рецепты с несколькими ингредиентами.

### Модель `RecipeIngredient`
- Используется как промежуточная таблица для связи "многие ко многим" между `Recipe` и `Ingredient`.
- В `Meta` установлено ограничение на уникальность связи рецепта и ингредиента (рецепт не может иметь один и тот же ингредиент более одного раза).

## Настройка панели администратора
Панель администратора позволяет управлять рецептами и ингредиентами через веб-интерфейс. Включена возможность добавления ингредиентов к рецепту с использованием `TabularInline` в админ-интерфейсе.

- **RecipeAdmin** — отображает рецепты и их ингредиенты в админке.
- **IngredientAdmin** — отображает список ингредиентов с полями `title`, `raw_weight`, `cooked_weight`, и `cost`.


### Заключение
Эта часть практической работы демонстрирует основные навыки создания и настройки моделей Django, панели администратора и представлений для отображения данных.